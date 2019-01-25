# QOS Policy
Module: ****arubaoss_qos_policy****  
Description: "This implements rest api's which can be used to configure qos on device."


##### ARGUMENTS
    class_name:
        description:
            - traffic class name
        required: false
    class_type:
        description:
            - traffic class type
        required: false
        choices: QCT_IP_V4, QCT_IP_V6
        default: QCT_IP_V4
    policy_name:
        description:
            - qos policy name
        required: true
    policy_type:
        description:
            - Type of qos. Onlye QOS_QPT is supported
        required: false
    action:
        description:
            - Type of qos action to take.
        requried: false
        default: QPAT_RATE_LIMIT
        choices: QPAT_RATE_LIMIT, QPAT_PRIORITY, QPAT_DSCP_VALUE
    action_value:
        description:
            - Value for each action.
        required: false
    sequence_no:
        description:
            - Sequence number for traffic class
        required: false


##### EXAMPLES
```YAML
      - name: create qos policy
        arubaoss_qos_policy:
          policy_name: my_qos
      - name: attach class to qos
        arubaoss_qos_policy:
          policy_name: my_qos
          class_name: my_class
          action: QPAT_RATE_LIMIT
          action_value: 1000
          sequence_no: "{{class_1.sequence_no}}"
      - name: delete qos policy
        arubaoss_qos_policy:
          policy_name: my_qos
          state: delete
```