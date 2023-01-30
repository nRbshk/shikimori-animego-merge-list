# shikimori-animego-merge-list

## basic usage
- import installed library `from shikimori_animego_merge_list import Converted`
- setup your usernames `user_animego, user_shikimori = 'your_animego_username', 'your_shikimori_username'
- you can collect your animes from animego or shikimori with next functions:
  ```python
  Converter.collectAnimegoUserAnime(user_animego) # save json tmp/{user_animego}_animego.json
  Converter.collectShikimoriUserAnime(user_shikimori) # save json tmp/{user_shikimori}_shikimori.json
  ```
- you can collect all animes from animego or shikimori with:
  ```python
  # do it once per season or if some title was update to the sites
  Converter.collectAllShikimori() # takes some time -> save json tmp/all_shikimori.json
  Converter.collectAllAnimego() # takes some time -> save json tmp/all_animego.json
  ```
## steps for merge animego list with shikimori
### steps
1) collect all shikimori animes from shikimori, which will be stores in `tmp/all_shikimori.json`
2) collect your animes from animego, which will be stores in `tmp/{username}_animego.json`
3) convert animego animes to shikimori animes, converted animes will be store in `tmp/{username}_converted_animego.json`, but some anime could not be find in shikimori, so they will be store in `tmp/{username}_not_converted_animego.json`. So you have to manual add it shikimori list
4) collect your animes from shikimori, which will be stores in `tmp/{username}_shikimori.json`
5) merge them, merged list will be stored in `tmp/merged.json`
### code
```python
from shikimori_animego_merge_list import Converter
user_animego, user_shikimori = 'your_animego_username', 'your_shikimori_username'

# step 1
Converter.collectAllShikimori() # do it once per season, no reasons for update it every time
# step 2
Converter.collectAnimegoUserAnime(user_animego)
# step 3
Converter.convertAnimegoToShikimori(user_animego)
# step 4
Converter.collectShikimoriUserAnime(user_shikimori)
# step 5
Converter.mergeAnimegoWithShikimori(user_animego, user_shikimori)
```
