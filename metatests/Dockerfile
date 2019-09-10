FROM jjc385/py3autograder

WORKDIR /autograder

COPY . /autograder/source
COPY ./setup.sh /autograder/
COPY ./run_autograder /autograder/

RUN chmod +x /autograder/setup.sh
RUN chmod +x /autograder/run_autograder
RUN apt-get update
RUN /autograder/setup.sh
