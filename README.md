## Running locally
1. Set up MAMP Server on Mac or WAMP Server if on Windows. 
2. Create a connection in Mysqlworkbench with host as localhost, port 3306, user root and password root. 
3. Execute notification.sql or merged_sql.sql
4. Run docker compose up -d --build from notifications folder
5. Head to notification_notification container to see the logs 
6. send a notification using the python manually_send_message.py in utils. Make sure to have the modules installed locally or in a virtual environment.
7. To tear down, use docker compose down. 

## Run tests
1. Run docker compose -f ci/docker-compose.test.yml up -d --build
2. Head to ci/ci_run_tests_1 container to view the results of the test.
3. To tear down, use docker compose -f ci/docker-compose.test.yml down