#
# Regular cron jobs for the oncilla-sim package
#
0 4	* * *	root	[ -x /usr/bin/oncilla-sim_maintenance ] && /usr/bin/oncilla-sim_maintenance
