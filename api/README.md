# API 

This is a RESTful API  to serve the data format.


## Usage

### Store

You must send a post request to: http://localhost:5000/store 
The body of your request must match the following template 

{
	"output_format": "json", 
	"fhir_resource_name": "patient"
}

### Mapping

You must send a post request to: http://localhost:5000/mapping 
The body of your request must match the following template 

{
	"output_format": "json", 
	"fhir_resource_name": "patient"
	"database": "CW"
}
