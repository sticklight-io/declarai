# Contribute :rocket:

Do you like **Declarai**?

Spread the word!

 - **Star** :star: the repository
 - **Share** the [link](https://github.com/vendi-ai/declarai) to the repository with your friends and colleagues
 - **Watch** the github repository to get notified about new releases.

## Development :material-source-pull:
Once you have cloned the repository, install the requirements:

Using `venv`

=== "Poetry"


    ```console
    poetry install
    ```


=== "Venv"


    ```console
    python -m venv env
    source env/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```


## Documentation :material-book-open-variant:

The documentation is built using [MkDocs](https://www.mkdocs.org/).
To view the documentation locally, run the following command:

<div class="termy">

```console
$ cd docs
$ mkdocs serve
INFO    -  [11:37:30] Serving on http://127.0.0.1:8000/
```
</div>

## Testing
The testing framework used is [pytest](https://docs.pytest.org/en/stable/).
To run the tests, run the following command:


```bash
pytest --cov=src   
```

## Pull Requests
It should be extermly easy to contribute to this project.
If you have any ideas, just open an pull request and we will discuss it.

```bash
git checkout -b my-new-feature
git commit -am 'Add some feature'
git push origin my-new-feature
```
