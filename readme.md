# This Project works with django as backend and react as frontend

We used 'flytech' and 'listing' projects codes as guidence. Such as how to send multiple serializers in
just on response to client requests and how to use custom 'lookup_field' for 'url' and multiple fields as
'read_only' and 'write_only' fields.

In the 'apis' app, for the 'Customer' model we use the 'name' field as lookup field as 'url' field in 'CustomerSerializer'.

IMPORTANT: We included 'migrations' and 'database' to the git project because of heroku stupidity.

We used DRF Validations in Serializers.
