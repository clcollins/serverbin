##### Signed by https://keybase.io/clcollins
```
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1

iEYEABECAAYFAlR1+ZQACgkQte6EFif3vzdD2QCfag4D+U2YL+jmP0N9BXhaV4ct
IxsAoPTNyH7JyjH+XzQOf5INgR2v+n6G
=hVaT
-----END PGP SIGNATURE-----

```

<!-- END SIGNATURES -->

### Begin signed statement 

#### Expect

```
size   exec  file                    contents                                                        
             ./                                                                                      
35120          LICENSE               fe3eea6c599e23a00c08c5f5cb2320c30adc8f8687db5fcec9b79a662c53ff6b
2301           README.md             34999b6c5d7cf0868405be1e2f448639db1108d915e3a35d42c6e7a36726b812
               apply_drupal_perms/                                                                   
1259             README.md           e309d90a716da45f69288cbadb45aa5c2e590f36778eee09d319ee0e9cb921da
3119   x         apply_drupal_perms  bc6e0783447879e6ef8589040b2339e250bbd5348762f47bbd85b4f07ef011a4
94               test.md             ada1eb0302130073156efd5324cee3a441023d34d7e1a971c2b560f8efd303cf
               apply_wp_perms/                                                                       
1351             README.md           bb365493e65b35aa9aac759893d56329b4ad2a5d1adc2084ca8e9691fb0021f3
3005   x         apply_wp_perms      ba643691f910163c6df47b813fe947f681755d3a746d7d6393fe2c9d95445f15
               hdafs/                                                                                
1763             README.md           5e911bb3c5830edde22ec545d4580642b909c1f87c775ac170b78cae4c84177c
2959   x         hdafs               fa310952d889e09f4666e4825af774f9642078511f04a0d3ddaa8d919a459192
               perms_by_conf/                                                                        
1096             README.md           d853acf508932ab9a929dfe8c16c61e375b0c95171df086aaa825dbc2edccfb1
238              example.yaml        c452554b0a1be79bf7ac572e40d03c69dae1632b3993bb86c50a074e321b4a2b
5270   x         perms_by_conf.py    692e1be2acde0c15c06bb4a69944d89be234ff612835a0b0fbcf9d0452dc2b60
               wp_report/                                                                            
1140             README.md           9d92e90c7345072fe34d87e4286ab7d32a7eaccc9a7407c0c2bf84a59cc70e97
2121   x         wp_report.py        eeefefa46b8e0f283135aab6a67ca8d94836ccb7d1b8e485d81a0c18821b55e8
```

#### Ignore

```
/SIGNED.md
```

#### Presets

```
git      # ignore .git and anything as described by .gitignore files
dropbox  # ignore .dropbox-cache and other Dropbox-related files    
kb       # ignore anything as described by .kbignore files          
```

<!-- summarize version = 0.0.9 -->

### End signed statement

<hr>

#### Notes

With keybase you can sign any directory's contents, whether it's a git repo,
source code distribution, or a personal documents folder. It aims to replace the drudgery of:

  1. comparing a zipped file to a detached statement
  2. downloading a public key
  3. confirming it is in fact the author's by reviewing public statements they've made, using it

All in one simple command:

```bash
keybase dir verify
```

There are lots of options, including assertions for automating your checks.

For more info, check out https://keybase.io/docs/command_line/code_signing