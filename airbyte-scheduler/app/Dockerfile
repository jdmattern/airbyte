ARG JDK_VERSION=14.0.2
FROM openjdk:${JDK_VERSION}-slim AS scheduler

ENV APPLICATION airbyte-scheduler

WORKDIR /app

ADD build/distributions/${APPLICATION}-0.30.31-alpha.tar /app

# wait for upstream dependencies to become available before starting server
ENTRYPOINT ["/bin/bash", "-c", "${APPLICATION}-0.30.31-alpha/bin/${APPLICATION}"]
