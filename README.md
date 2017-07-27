# Foreign Tongue

Randomly generate a human-like langauge.

Requires python 3.

```python3
from foreigntongue import Language, get_latin, get_ipa

lang = Language()
get_latin(lang.get_word(pos='NN', english='fish'))
# 'ah'

get_ipa(lang.get_word(pos='NN', english='fish'))
# 'ɑʔ'
```
