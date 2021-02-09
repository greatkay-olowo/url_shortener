#Url Shortner

A url shortener that shortens url and records hits when redirecting.

## Installation

Download the code from [greatkay-olowo github]().
then:
```
pip install
```

## Usage

### Shorten url
```
GET /new/{url}
```
### redirect url
```
GET /{code}
```
### show record
```
GET /record/{code}
```