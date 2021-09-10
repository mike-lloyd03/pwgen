#!/usr/local/bin/python3
from os import path
import random
import fire


class PasswordGenerator:
    def __init__(
        self,
        word_list="./wordlist",
        min_word_length=5,
        max_word_length=10,
        n_words=3,
        title_caps=False,
        all_caps_last_word=False,
        separator="-",
    ):
        self.min_word_length = min_word_length
        self.max_word_length = max_word_length
        self.n_words = n_words
        self.title_caps = title_caps
        self.all_caps_last_word = all_caps_last_word
        self.separator = separator

        self.word_list = self._load_word_list(word_list)
        if len(word_list) < self.n_words:
            raise InputError(
                "The word list file has less words than the minimum number of words per password"
            )

    def _load_word_list(self, word_list_file):
        with open("wordlist") as f:
            word_list = [
                word.strip().replace("\n", "").replace(" ", "")
                for word in f.readlines()
            ]
        return word_list

    def _get_random_word(self):
        word = random.choice(self.word_list)
        if len(word) < self.min_word_length:
            word = self._get_random_word()
        if len(word) > self.max_word_length:
            word = self._get_random_word()
        return word

    def _build_passwd_list(self):
        passwd_list = [self._get_random_word() for i in range(self.n_words)]
        # Check that no words are duplicated
        if len(set(passwd_list)) != len(passwd_list):
            passwd_list = self._build_passwd_list()
        return passwd_list

    def generate(self):
        passwd_list = self._build_passwd_list()
        if self.title_caps:
            passwd_list = [word.capitalize() for word in passwd_list]
        if self.all_caps_last_word:
            passwd_list[-1] = passwd_list[-1].capitalize()
        return self.separator.join(passwd_list)


def generate(
    word_list="./wordlist",
    min_word_length=5,
    max_word_length=10,
    n_words=3,
    title_caps=False,
    all_caps_last_word=False,
    separator="-",
):
    """generate a random password with the given inputs"""
    pg = PasswordGenerator(
        word_list=word_list,
        min_word_length=min_word_length,
        max_word_length=max_word_length,
        n_words=n_words,
        title_caps=title_caps,
        separator=separator,
    )
    return pg.generate()


if __name__ == "__main__":
    fire.Fire(generate, name="generate")
