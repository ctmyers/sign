The bus plugin is designed to get the time of arrival for the next two busses at a given stop
The config file looks like this

agency=<location>
stop_id=<stop id, its an integer>
ignore_routes=<a comma separated list of stop numbers to ignore>

for example:
agency=umd
stop_id=29789
ignore_routes=127,125,131


The stop id and route numbers can be found at nextbus.com