# ARUBAOS GET

Module: **arubaos_get**
Description: Executes GET operations on API objects

### ARGUMENTS
    host:
        description:
            - Hostname or IP Address of the controller.
            - If not set the environment variable C(ANSIBLE_ARUBAOS_HOST) will be used.
        required: true
        type: str
        fallback: ANSIBLE_ARUBAOS_HOST
    username:
        description:
            - Username used to login to the controller.
            - If not set the environment variable C(ANSIBLE_ARUBAOS_USERNAME) will be used.
        required: true
        type: str
        fallback: ANSIBLE_ARUBAOS_USERNAME
    password:
        description:
            - Password used to login to the controller.
            - If not set the environment variable C(ANSIBLE_ARUBAOS_PASSWORD) will be used.
        required: true
        type: str
        no_log: true
        fallback: ANSIBLE_ARUBAOS_PASSWORD
    validate_certs:
        description:
            - Set to True to validate server SSL certificate upon HTTPS connection. Default option is false.
        required: false
        type: str
        default: None
    client_cert:
        description:
            - Set the file path for client certificate validation from server side. Default option is None.
        required: false
        type: str
        default: None
    client_key:
        description:
            - If the client_cert did not have the key, use this parameter. Default option is None.
        required: false
        type: str
        default: None
    object:
        description:
            - Name of the object type which needs to be queried.
        type: str
        required: true
    config_path:
        description:
            - Complete config-node or config-path from which the information should be retrieved.
            - On a managed device this will be restricted to /mm/mynode.
            - On a stand-alone controller, this will be restricted to /mm and /mm/mynode.
        required: false
        type: str
        default: None
    sort:
        description:
            - Sorts the returned object based on specified paramter and order
            - There can only be one sort filter per request.
            - Single string of th form <operator><parama_name>.
            - Operator can be C(+) for ascending or C(-) for descending.
            - Param name is a fully qualified attribute name.
        type: str
        required: false
    offset:
        description:
            - Conveys the index (1 based) from which the returned data set should start.
            - Must be a multiple of I(limit) plus one. In other words, offset % limit = 1.
            - Required together with I(limit).
        type: int
        required: false
        default: None
    limit:
        description:
            - Maximum number of objects returned.
            - Required together with I(offset).
        type: int
        required: false
        default: None
    total:
        description:
            - Expected total count of objects before any pagination applied by I(limit) and I(offset).
            - If the actual total doesnt match this value, returned data set will contain a dirty flag.
            - Can be used to check if objects were created or delted between two paginated requests.
        type: int
        required: false
        default: None
    count:
        description:
            - Requests the API to include a count of specified objects or parameters along with the object data.
            - Elements should be fully qualified names of objects or attributes.
        type: list
        elemets: str
        required: false
        default: []
    data_types:
        description:
            - Filters returned objects based on configuration state.
            - Only applies to top level objects in the query.
            - Mutually exclusive with I(object_filters) and I(data_filters).
        type: list
        required: false
        default: []
        choices: [non-default, default, local, user, system, pending, committed, inherited, meta-n-data, meta-only]
    object_filters:
        description:
            - Filters returned objects based on object type.
            - Mutually exclusive with I(data_types).
        type: list
        elements: dict
        required: false
        default: []
        suboptions:
            oper:
                description:
                    - Operation to be applied on the filter values.
                required: true
                type: str
                choices: [$eq, $neq]
            values:
                description:
                    -  List of fully qualified object names to be matched by the filter.
                required: true
                type: list
                elements: str
    data_filters:
        description:
            - Filters returned objects based on object attributes.
            - Mutually exclusive with I(data_types).
        type: list
        elements: dict
        required: false
        default: []
        suboptions:
            param_name:
                description:
                    - Fully qualified name of the parameter to be looked up by the filter.
                required: true
                type: str
            oper:
                description:
                    - Operation to be applied on the filter values.
                required: true
                type: str
                choices: [$eq, $neq, $gt', $gte, $lt, $lte, $in, $nin]
            values:
                description:
                    -  List of values to be matched by the filter.
                required: true
                type: list
                elements: str

### RETURN

    response:
        description: Data set returned by the GET request.
        returned: on success

### EXAMPLES

```YAML
environment:
  ANSIBLE_ARUBAOS_HOST: 192.168.1.1
  ANSIBLE_ARUBAOS_USERNAME: admin
  ANSIBLE_ARUBAOS_PASSWORD: aruba123

tasks:

  - name: Get AAA profiles
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1

  - name: Get AAA profiles configured locally and in a commited state
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      data_types: [local, commited]

  - name: Get AAA profiles, but only return server_group sub-objects
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      object_filters:
        - oper: $eq
          values: [aaa_prof.server_group]

  - name: Get AAA profiles with profile-name containing 'corp' or 'guest'
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      data_filters:
        - parama_name: aaa_prof.profile-name
          oper: $in
          values: [corp, guest]

  - name: Get the the number of server groups configured on aaa profile named 'guest'
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      data_filters:
        - parama_name: aaa_prof.profile-name
          oper: $eq
          values: [guest]
      count: [aaa_prof.server_group]

  - name: Get the first 10 AAA profiles sorted by profile name
    arubaos_get:
      object: aaa_prof
      config_path: /md/branch1/building1
      limit: 10
      offset: 1
      sort: +aaa_prof.profile-name
```

