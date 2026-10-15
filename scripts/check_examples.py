"""Validate documentation examples, not a live service or a complete OpenAPI schema."""
from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = yaml.safe_load((ROOT / 'docs/assets/openapi.yaml').read_text(encoding='utf-8'))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def resolve(schema):
    while '$ref' in schema:
        node = spec
        for part in schema['$ref'].removeprefix('#/').split('/'):
            node = node[part]
        schema = node
    return schema

def validate(value, schema):
    schema = resolve(schema)
    kind = schema['type']
    if kind == 'object':
        require(isinstance(value, dict), 'Expected object')
        require(set(schema.get('required', [])) <= value.keys(), 'Missing required field')
        if schema.get('additionalProperties') is False:
            require(value.keys() <= schema['properties'].keys(), 'Unknown field')
        for key, item in value.items():
            if key in schema.get('properties', {}):
                validate(item, schema['properties'][key])
    elif kind == 'string':
        require(isinstance(value, str), 'Expected non-null string')
        length = (len(value.encode('utf-16-le')) // 2
                  if schema.get('x-length-unit') == 'UTF-16-code-units' else len(value))
        require(length >= schema.get('minLength', 0), 'String too short')
        require(length <= schema.get('maxLength', float('inf')), 'String too long')
        require(re.search(schema.get('pattern', ''), value) is not None, 'Invalid string pattern')
    elif kind == 'integer':
        require(type(value) is int, 'Expected integer')
        require(schema.get('minimum', float('-inf')) <= value <= schema.get('maximum', float('inf')),
                'Integer out of range')
    else:
        raise ValueError(f'Unsupported schema type: {kind}')
    if 'enum' in schema:
        require(value in schema['enum'], 'Unexpected enum value')

def main():
    operation = spec['paths']['/tasks']['post']
    require(spec['info']['version'] == '1.0.0', 'Unexpected contract version')
    mapping = [('request', 'CreateTask'), ('task', 'Task'), ('problem', 'Problem')]
    fixtures = {}
    for name, schema_name in mapping:
        data = json.loads((ROOT / f'docs/assets/{name}.json').read_text(encoding='utf-8'))
        validate(data, spec['components']['schemas'][schema_name])
        fixtures[name] = data
    require(operation['requestBody']['content']['application/json']['example'] == fixtures['request'],
            'OpenAPI request example differs')
    for status, media, name in [('201', 'application/json', 'task'),
                                ('400', 'application/problem+json', 'problem')]:
        require(operation['responses'][status]['content'][media]['example'] == fixtures[name],
                f'OpenAPI {status} example differs')
    count = 0
    for path in (ROOT / 'docs/examples').glob('*.md'):
        text = path.read_text(encoding='utf-8')
        for raw in re.findall(r'```json\n(.*?)\n\s*```', text, re.S):
            data = json.loads(raw)
            name = 'problem' if 'type' in data else 'task' if 'id' in data else 'request'
            require(data == fixtures[name], f'{path.name}: JSON differs from fixture {name}')
            count += 1
        for raw in re.findall(r"--data '([^']+)'", text):
            require(json.loads(raw) == fixtures['request'], f'{path.name}: curl body differs')
    require(count >= 3, 'Expected at least three JSON blocks')
    require(set(operation['responses']) == {'201', '400', '401', '403', '415'}, 'Unexpected statuses')
    print(f'OK: 3 fixtures, OpenAPI examples, {count} Markdown JSON blocks and curl bodies')

if __name__ == '__main__':
    main()
