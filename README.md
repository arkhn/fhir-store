[![Build Status](https://travis-ci.com/arkhn/fhir-store.svg?branch=master)](https://travis-ci.com/arkhn/fhir-store)
[![GitHub license](https://img.shields.io/github/license/arkhn/fhir-pipe.svg)](https://github.com/arkhn/fhir-pipe/blob/master/LICENSE)
[![Website arkhn.org](https://img.shields.io/website-up-down-green-red/https/arkhn.org.svg)](http://arkhn.org/)

# FHIR Store: the FHIR standard in your favourite format

FHIR Store provides the FHIR standard in several formats, including `json` and `yml`.

## `yml` standard

We have converted the FHIR specification available [on this hl7 page](https://www.hl7.org/fhir/resourcelist.html) (See **R2 Layout** tab) into the `yml` format.

The folders follows the hierarchy described in the R2 Layout, and an additional folder `DataTypes` retrieves the complex types detailed [on this hl7 page](https://www.hl7.org/fhir/datatypes.html)

 Note that the **`json` format** is also available, which can be more easy for api calls. Oh, actually we already built an API [just here](https://github.com/arkhn/fhir-ball-server)!


### Typing convention
The FHIR standard has a structure of a tree. We have typed each node, which can be a simple type (eg `deceasedBoolean<boolean>` or `birthDate<date>`). One basic type which is worth explaining is `code`, which is used like this: `gender<code=male|female|other|unknown>`. If no type is provided, we assume it is a string. You can also have special `DataType` (eg `HumanName`, `ContactPoint`, `Address`, [see complete list](https://www.hl7.org/fhir/datatypes.html)) which follows the same convention (eg `address<Address>`). If the node is a list, we add `list::` in the typing, like in `telecom<list::ContactPoint>`. Note that for the case of a list of strings we will have `node<list>`. 

### Bindings conventions 

You have 4 options to link a FHIR attribute to SQL resources, which can be combined. Have a look in the `fhir-mapping` project at `Identification/Individuals/Patient.yml` to see these examples used in a real context.

1. **_col**: the name of the column where the information is visible. You should specify `<OWNER>.<TABLE>.<COLUMN>`. You can put several items in a list if the information is dispatched.
2. **_script**: the name of the script that you apply on the `_col` items to clean the data. For phone it is `clean_phone`, etc; if none just put `equal`. Usually you have 1 script for 1 col, but in the case where you have 1 script and n>1 cols, then all the cols are given as arguments to the script.
3. **_join**: if the information is not available in the "root" table (eg `ICSF.PATIENT` for Resource Patient), you specify the join to do on another table to get the info. Join has two attributes, 
    * **_type** which specifies the nature of the join (OneToOne, OneToMany, etc) and
    * **_args** which details how to join with the format `["<owner>.<table>.<col>=<owner>.<join_table>.<join_col>"]`.
4. **\_template_id**: when the node is of a special `DataType` (eg `HumanName`, `ContactPoint`, `Address`, etc), the description of each subfile will be made in the `yml` file which has the same name, in a _template_ referenced by an ID. This helps having a short Resource mapping file. 

## How to start

We have reported several issues with the label `Good first issue` which can be a good way to start! Also of course, feel free to contact us on Slack in you have trouble with the project.

If you're enthusiastic about our project, :star: it to show your support! :heart:

* * *

## License

[Apache License 2.0](https://github.com/OpenMined/PySyft/blob/master/LICENSE)
