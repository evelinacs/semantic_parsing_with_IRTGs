# Prerequisites

- python3
- the `nltk` package

# Usage

```shell
> python generate_grammar.py tree_file dependency_file > output.irtg
```

- `tree_file`: output of `code/generate_input_from_trees/extract_subtrees.py` with sanitize option
- `dependency_file`: the output of parsing `tree_file` with the Stanford parser
- `output.irtg`: contains the interpretation definitions, a start rule and conversion rules; terminal rules must be appended separately

# Test input

Minimal test inputs can be found in the `test_data` folder.
