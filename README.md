# PV-Simulator

This application generates simulated PV(photovoltaic) power	values(in KW).
This system consists of a meter, a broker and a PV simulator. RabbitMQ is used as the broker.

### Prerequisites

**NOTE:** Make sure you have [Docker] and [Docker Compose] installed.
Meter and PV Simulator services install the required modules listed int the requirements.txt.

## Getting Started
To start all the services go through the following steps:

```bash
    $ git clone git@github.com:Mina-Momenzadeh/PV-Simulator.git
    $ cd pv_simulator
    $ docker-compose up
```

After doing these steps 3 containers(rabbitmq, pv_sim, meter_sim) are started. pv_sim and meter_sim
are bound to RabbitMQ so they will try untill the rabbitmq is started.

After running you can check the process on each container.
* The output file is **output.txt** and is located in the output folder on pv-sim container.
* Meter keeps the track of generated data on its container in the **meter.log** file in the log folder.
