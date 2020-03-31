import logging

import pandas as pd

from data import load_dataset
from sdgym.evaluate import evaluate

LOGGER = logging.getLogger(__name__)


DEFAULT_DATASETS = [
    "adult",
    "alarm",
    "asia",
    "census",
    "child",
    "covtype",
    "credit",
    "grid",
    "gridr",
    "insurance",
    "intrusion",
    "mnist12",
    "mnist28",
    "news",
    "ring"
]


def benchmark(synthesizer, datasets=DEFAULT_DATASETS, repeat=3):
    results = list()
    for name in datasets:
        LOGGER.info('Evaluating dataset %s', name)
        train, test, meta, categoricals, ordinals = load_dataset(name, benchmark=True)
        

        for iteration in range(repeat):
            synthesized = synthesizer(train, categoricals, ordinals)
            print(synthesized)
            print(train)
            print(meta)
            print(test)
            scores = evaluate(train, test, synthesized, meta)
            print(scores)
            scores['dataset'] = name
            scores['iter'] = iteration
            results.append(scores)

    return pd.concat(results)
