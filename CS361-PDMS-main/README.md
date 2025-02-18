# Personal Data Management Service (PDMS) - Communication contracts

## Index

* [Specifications](#Specifications)
* [Sequence diagrams](#Sequences)
* [API Specifications](#API-specifications)

## Basic Information
* CS361, 2025 Winter term
* Developer name: Takafumi Suzuki

## How to use this service
Main programs can communicate with this service via <span style="color: red;">**ZeroMQ**</span> in the local environment.<br>
The port number of this service is <span style="color: red;">**#5555**</span>.

### 1.How to request data

To request data from this service, main programs must create requests in the specified format and a socket with the port number, then send it.<br>

Request Specification:

| Attribute | Meaning                                                                                         |
|-----------|-------------------------------------------------------------------------------------------------|
| request   | Top level attribute, which must include event and body attributes.                              |
| event     | The name of event used to invoke functions related to each user story.                          |
| body      | The data to be used in functions related to user stories. The value varies depending on events. |

Example:
```
{
    "request": {
        "event": "customerAgeData",
        "body": ""
    }
}
```

### 2.How to receive data

To retrieve data from this service, main programs must create a socket for receiving beforehand.<br>
After sending the request, your main program receive a response in the following format.<br>

Response Specification:

| Attribute | Meaning                                                                   |
|-----------|---------------------------------------------------------------------------|
| response  | Top level attribute, which must include event, body, and code attributes. |
| event     | The name of event used to invoke functions related to each user story.    |
| body      | The data returned from this service.                                      |
| code      | Response status. In the case of success, its value is 200, otherwise 400. |

Example:
```
{
    "response": {
        "event": "customerAgeData",
        "body": {
            "customerAge": ["18", "25", "33", "45"]
        },
        "code": "200"
    }
}
```

## Sequences
### Controller

```plantuml
@startuml

' Participants
Participant "Main Program" as main
Participant "PDMS" as pdms #LightGreen

' Flow
activate main

main -> pdms: Send a request via ZeroMQ

activate pdms

pdms -> pdms: parse the request
activate pdms
deactivate pdms

alt event == getLaborCost
    ref over pdms: See the sub-sequence of getLaborCost event
else event == postLaborData
    ref over pdms: See the sub-sequence of postLaborData event
else event == getLaborData
    ref over pdms: See the sub-sequence of getLaborData event
else event == customerAgeData
    ref over pdms: See the sub-sequence of customerAgeData event
end

pdms -> pdms: create a response
activate pdms
deactivate pdms

pdms -> pdms: create a socket for main programs
activate pdms
deactivate pdms

main <- pdms: Send a response via ZeroMQ

deactivate pdms
deactivate main
@enduml
```

### getLaborCost event
```plantuml
@startuml

' Participants
Participant Controller as cont #LightGreen
Participant getLaborCostUsecase as uc #LightGreen

activate cont

cont -> cont: create the instance of \ngetLaborCostUsecase class
cont -> uc: execute()

activate uc
uc -> uc: parse the body of a request
activate uc
deactivate uc

uc -> uc: calculate the total labor costs
activate uc
deactivate uc

alt succeed in calculation
    uc -> uc: set status code = 200
    activate uc
    deactivate uc
else
    uc -> uc: set status code = 400
    activate uc
    deactivate uc
end

cont <- uc: return the total labor cost and status code

deactivate uc
deactivate cont
@enduml
```

### postLaborData event
```plantuml
@startuml

' Participants
Participant Controller as cont #LightGreen
Participant postLaborDataUsecase as uc #LightGreen
database LaborData as db

activate cont

cont -> cont: create the instance of \npostLaborDataUsecase class
cont -> uc: execute()

activate uc
uc -> uc: parse the body of a request and get
activate uc
deactivate uc

uc -> db: save the labor data to DB

note right
 DB is a csv file format.
 File path: ../labors_data.csv
end note

alt succeed in updating the DB
    uc -> uc: set status code = 200
    activate uc
    deactivate uc
else
    uc -> uc: set status code = 400
    activate uc
    deactivate uc   
end

cont <- uc: return status code

deactivate uc
deactivate cont
@enduml
```

### getLaborData event
```plantuml
@startuml

' Participants
Participant Controller as cont #LightGreen
Participant getLaborDataUsecase as uc #LightGreen
database LaborData as db

activate cont

cont -> cont: create the instance of \ngetLaborDataUsecase class
cont -> uc: execute()

activate uc
uc -> uc: get a leader name
activate uc
deactivate uc

uc -> db: get labor data that matches the leader name
activate db
uc <- db: return labor data
deactivate db

note right
 DB is a csv file format.
 File path: ../labors_data.csv
end note

alt succeed in retrieving data
    uc -> uc: set status code = 200
    activate uc
    deactivate uc
else
    uc -> uc: set status code = 400
    activate uc
    deactivate uc
end

cont <- uc: return labor data and status code

deactivate uc
deactivate cont
@enduml
```

### customerAgeData event
```plantuml
@startuml

' Participants
Participant Controller as cont #LightGreen
Participant customerAgeDataUsecase as uc #LightGreen
database customerData as cd

activate cont

cont -> cont: create the instance of \ncustomerAgeDataUsecase class
cont -> uc: execute()

activate uc

uc -> cd: get customer data
activate cd
cd -> uc: return customer data
deactivate cd

alt DB is empty
    uc -> uc: set status code = 400
    activate uc
    deactivate uc
else

    uc -> uc: extract customer ages
    activate uc
    deactivate uc

    uc -> uc: set status code = 200
    activate uc
    deactivate uc
end

note right
 DB is a csv file format.
 File path: ../customers_data.csv
end note

cont <- uc: return customer ages and status code

deactivate uc
deactivate cont
@enduml
```

## API-specifications
### getLaborCost event
#### request sample
```commandline
{
    "request": {
        "event": "getLaborData",
        "body": {
            "crewName": "Andrew"
        }
    }
}
```
#### response sample
```commandline
{
    "response": {
        "event": "getLaborData",
        "body": {
          "labor": {
            "Worker": ["5","20"],
            "CrewLead": ["1", "28"],
            "Supervisor": ["1","32"]
          }
        },
        "code": "200"
    }
}
```

### postLaborData event
#### request sample
```commandline
{
    "request": {
        "event": "postLaborData",
        "body": {
          "crewName": "Andrew",
          "labor": {
            "Worker": ["5","20"],
            "CrewLead": ["1", "28"],
            "Supervisor": ["1","32"]
          }
        }
    }
}
```
#### response sample
```commandline
{
    "response": {
        "event": "postLaborData",
        "body": "",
        "code": "200"
    }
}
```

### getLaborData event
#### request sample
```commandline
{
    "request": {
        "event": "getLaborData",
        "body": {
            "crewName": "Andrew"
        }
    }
}
```
#### response sample
```commandline
{
    "response": {
        "event": "getLaborData",
        "body": {
          "labor": {
            "Worker": ["5","20"],
            "CrewLead": ["1", "28"],
            "Supervisor": ["1","32"]
          }
        },
        "code": "200"
    }
}
```

### customerAgeData event
#### request sample
```commandline
{
    "request": {
        "event": "customerAgeData",
        "body": ""
    }
}
```
#### response sample
```commandline
{
    "response": {
        "event": "customerAgeData",
        "body": {
            "customerAge": ["18", "19", "18"]
        },
        "code": "200"
    }
}
```

