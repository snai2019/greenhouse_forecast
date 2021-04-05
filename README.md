# Deploying and Hosting a Forecasting Model with FastAPI 

## Want to learn how to build this?

Check out the [post]().

## Want to use this project?

1. Create and activate a virtual environment:
a. Create new virtual environment with conda or virtualenv

conda create -n env_name 
activate env_name

or Open Anaconda -> Create new env -> Open conda terminal

b. Install requirements.txt

pip install -r requirements.txt

conda install -r requirements.txt

c. For fbprophet
On Prompt install Ephem:
conda install -c anaconda ephem

Install Pystan:
conda install -c conda-forge pystan

Finally install Fbprophet
conda install -c conda-forge fbprophet

Note that fbprophet support python < 3.8

2. Install the requirements:

    ```sh
    (env_name)$ pip install -r requirements.txt
    ```

3. Train the model:

    ```sh
    (env_name)$ python

    >>> from model import train, predict, convert
    >>> train()
    ```

4. Run the app:

    ```sh
    (env_name)$ uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8008
    ```

5. Test:

    ```sh
    $ curl -X POST "http://127.0.0.1:8000/predict" 
    -H  "accept: application/json" 
    -H  "Content-Type: application/json" 
    -d "{\"parameter\":\"Co2-121\",\"hours\":3}"
    ```
