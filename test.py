def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_forms(cldf_dataset):
    assert len(list(cldf_dataset["FormTable"])) == 1401


def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 173


def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 7
