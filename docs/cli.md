### How to use the upgraded CLI

By adjusting the router, your data recovery and server environments can now push specific clinical requests through the HPC architecture using the same normalized JSON schemas produced by the Univac-IX bridge.

**Track Variant Species Encystment (Original):**

Bash

```
python main_cli.py --ehr data/hpc_batch_queue/ --mode oncology --cores 32 --cuda

```

**Evaluate Point Stress & Hemorrhage:**

Bash

```
python main_cli.py --ehr data/hpc_batch_queue/ --mode trauma --tip-radius 4.2 --cores 32

```

**Run Cardiac & Metabolic Benchmarks:**

Bash

```
python main_cli.py --ehr data/hpc_batch_queue/ --mode metabolism --cores 32
```
