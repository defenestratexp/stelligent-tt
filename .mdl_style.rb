# Markdown lint style for this course.
all
# TOC entries, URLs and exam tables can't reasonably wrap at 80 columns.
exclude_rule 'MD013'
exclude_rule 'MD007'
# Lists may be numbered 1. 1. 1. or 1. 2. 3., and nested lists under a
# numbered item align with its text (3 spaces). Both render correctly.
exclude_rule 'MD029'
exclude_rule 'MD005'
# Lab questions are headings that end in "?".
rule 'MD026', :punctuation => '.,;:!'
# The course README opens with the logo image.
exclude_rule 'MD041'
