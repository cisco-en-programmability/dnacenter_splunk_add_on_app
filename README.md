# Cisco DNA Center Add-On App for Splunk Enterprise


This Python script collects device inventory and overall network health using the Cisco DNA Center REST APIs.

**Cisco Products & Services:**

- Cisco DNA Center
- Cisco Network Devices Managed by Cisco DNA Center

**Tools & Frameworks:**

- Splunk Enterprise Server

**Usage**

Knowledge of creating Splunk Add-On Apps is required.
It is recommended to have a recurring schedule for the app to collect real time data from Cisco DNA Center.

The repo includes:
 - dnac_rest_apis.py - code that will run on Splunk Enterprise to collect the device inventory (used for reachability
 reporting), and device health
 - dnacenter_splunk_dashboard.xml - sample Splunk dashboard that will display real time:
   - summary device health, during the past 60 minutes
   - device reachability, during the past 60 minutes
   - events received from Cisco DNA Center, during the past 30 days

Splunk Dashboard:
!(https://github.com/cisco-en-programmability/dnacenter_splunk_add_on_app/blob/master/Cisco_DNA_Center_dashboard.png?raw=true)


**License**

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
