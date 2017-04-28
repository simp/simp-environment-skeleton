#!/bin/sh -x

(
  cd `dirname $0`;

  /bin/rm -f .ca_run_lock;
  /bin/rm -rf demoCA;
  /bin/rm -rf working;
  /bin/rm -rf output;
  /bin/rm -f cacertkey;
  /bin/rm -f CA;
  /bin/rm -f CA_batch;
)
