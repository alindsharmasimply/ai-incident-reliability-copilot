## Tests Execution
- Faced a few issues while setting-up and running the tests:
    - The '/tests' folder wasn't copied in the Dockerfile hence wasn't able to locate.
    - The testing command now needs to execute with a dedicated PYTHONPATH
