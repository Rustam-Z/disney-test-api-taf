# Disney's API Test Automation Framework

## Configuration 
1. Edit `.config.yaml`.
   Config file includes `API `
   If you change the content and schema of this file, you need to change following files too. 
   ```text
   /core/enums/environments.py # The list of env: DEV, STAGING, PROD.
   /core/config/__init__.py # Change this file, if you change the schema of config file.
   /tests/conftest.py # Change PyTest hooks.
   /paths.py # The paths for common project files. Change here if you edit the name of config file.
   ```

## Constraints
```text
1. @mobile() # Fixture for mobile which uses `/?is_for_mobile=true`
2. Auth -> auth, unauth requests. We will not separate users. Because super user has different request body.
3. Endpoints, endpoints with schema, response model. We will not create request model.
```

## Project structure
```text
`core` will include anything related to framework.
`api` will contain anything related to API, enums, models, resources, query string params.
`tests` will contain all tests.
```