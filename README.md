# Disney's API Test Automation Framework

## Configuration 
1. `.config.yaml` includes `API URLs` for DEV, STAGING and PROD envs. 
   It includes users credentials for superuser, facility admin, facility driver, facility simple user.
   - Superuser -> can control all facilities. Superuser can create a new facility, and facility admin.
   - Facility admin -> can control all users only for his/her facility. 
   - Facility driver -> this type of user, has driver user role.
   - Facility user -> this type of user has limited edit, view authorization only for assigned facility. 
2. If you change the content and schema of config file, you need to change following files too:
   ```text
   /core/enums/environments.py # The list of env: DEV, STAGING, PROD.
   /core/config/__init__.py # Change this file, if you change the schema of config file.
   /tests/conftest.py # Change PyTest hooks.
   /paths.py # The paths for common project files. Change here if you edit the name of config file.
   ```

## Constraints
```text
1. @mobile() # Fixture for mobile which uses `/?is_for_mobile=true`
2. Authentication -> auth, unauth requests. We will not separate users. Because super user has different request body.
3. Endpoints, endpoints with schema, request & response model.
```

## Project structure
```text
`core` will include anything related to framework.
`api` will contain anything related to API, enums, models, resources, query string params.
`tests` will contain all tests.
```

## Response validation plan
1. Validate HTTP status code
2. Validate schema: convert response.json() to pydantic model to check data types, and verify that all fields are present. 
   1. `status` and `message` fields content are checked via pydantic.
   2. Error messages content for error responses are checked via pydantic.
3. Validate data, and assert result with expected.


## How to write test for new feature?
1. Learn new feature, create test scenarios, test cases.
2. Create success & error response models in `api/responses`.
3. Create requests, API services, helper functions in `api/requests`. Validate status code, schema inside these helpers.
4. Write tests in `tests` folder.
