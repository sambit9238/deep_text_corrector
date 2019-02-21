"""Preprocesses Cornell Movie Dialog data."""
import tensorflow as tf

tf.app.flags.DEFINE_string("raw_data", "", "Raw data path")
tf.app.flags.DEFINE_string("out_file", "", "File to write preprocessed data "
                                           "to.")

FLAGS = tf.app.flags.FLAGS

def replace_contraction(text):
    contraction_patterns = [ (r'won\'t', 'will not'), (r'can\'t', 'can not'), (r'i\'m', 'i am'), (r'ain\'t', 'is not'), (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'),
                         (r'(\w+)\'ve', '\g<1> have'), (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would'), (r'&', 'and'), (r'dammit', 'damn it'), (r'dont', 'do not'), (r'wont', 'will not') ]
    patterns = [(re.compile(regex), repl) for (regex, repl) in contraction_patterns]
    for (pattern, repl) in patterns:
        (text, count) = re.subn(pattern, repl, text)
    return text
def replace_links(text, filler='links'):
        text = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
                      filler, text).strip()
        return text

import re
def cleanText(text):
    text = text.strip().replace("\n", " ").replace("\r", " ")
    text = replace_contraction(text)
    text = replace_links(text, "link")
    text = text.lower()
    return text

def main(_):
    with open(FLAGS.raw_data, "r", encoding="latin1") as raw_data, \
        open(FLAGS.out_file, "w", encoding="latin1") as out:
        for line in raw_data:
            parts = line.split(" +++$+++ ")
            dialog_line = parts[-1]
            s = cleanText(dialog_line)
            out.write(s + "\n")
    with open(FLAGS.out_file, "r", encoding="latin1") as out, \
        open("train.txt","w", encoding="latin1") as train1, \
        open("test.txt", "w", encoding="latin1") as test1:
        for lineno, line in enumerate(out):
            if lineno < 300000:
                train1.write(line)
            else:
                test1.write(line)


if __name__ == "__main__":
    tf.app.run()
