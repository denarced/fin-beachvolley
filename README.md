# fin-beachvolley
Parse Finnish beach volleyball site.

# Example
````shell
(venv) $ python parse.py -i 'pojat 18' 'jnbt miehet' -d | column -t -s'  '
Thu 2024-06-06  Thu 2024-06-06  Joensuu                  Pojat 18
|               |               |                        |
Sat 2024-06-08  Sat 2024-06-08  Kokkola                  JNBT miehet
Sun 2024-06-09  Sun 2024-06-09  Turku                    JNBT miehet
|               |               |                        |
Thu 2024-06-13  Thu 2024-06-13  Sastamala P18            Pojat 18
|               |               |                        |
Sat 2024-06-15  Sat 2024-06-15  Sastamala Open           JNBT miehet
Sun 2024-06-16  Sun 2024-06-16  Nivala                   JNBT miehet
Sun 2024-06-16  Sun 2024-06-16  Eura P18                 Pojat 18
|               |               |                        |
Wed 2024-06-19  Wed 2024-06-19  Tampere P18              Pojat 18
|               |               |                        |
Sat 2024-06-29  Sat 2024-06-29  Jyväskylä                JNBT miehet
Sun 2024-06-30  Sun 2024-06-30  Hanko                    JNBT miehet
Mon 2024-07-01  Mon 2024-07-01  Jyväskylä P18            Pojat 18
|               |               |                        |
Thu 2024-07-04  Thu 2024-07-04  Helsinki Hietsu          JNBT miehet
|               |               |                        |
Sat 2024-07-06  Sat 2024-07-06  Kouvola                  JNBT miehet
Sat 2024-07-06  Sat 2024-07-06  Helsinki P18             Pojat 18
Sun 2024-07-07  Sun 2024-07-07  Vaala                    JNBT miehet
|               |               |                        |
Thu 2024-07-11  Thu 2024-07-11  Kalajoki P18             Pojat 18
|               |               |                        |
Sat 2024-07-13  Sat 2024-07-13  Kalajoki                 JNBT miehet
Sat 2024-07-13  Sat 2024-07-13  Savonlinna               JNBT miehet
Sun 2024-07-14  Sun 2024-07-14  Vaasa P18                Pojat 18
|               |               |                        |
Thu 2024-07-18  Thu 2024-07-18  Hyvinkää P18             Pojat 18
|               |               |                        |
Sun 2024-07-21  Sun 2024-07-21  Beachbox Helsinki        JNBT miehet
Sun 2024-07-21  Sun 2024-07-21  Kempele P18              Pojat 18
|               |               |                        |
Sat 2024-07-27  Sat 2024-07-27  Turku P18                Pojat 18
Sun 2024-07-28  Sun 2024-07-28  Joensuu                  JNBT miehet
|               |               |                        |
Sat 2024-08-03  Sat 2024-08-03  Raahe                    JNBT miehet
Sat 2024-08-03  Sat 2024-08-03  Soisalo Open Leppävirta  JNBT miehet
Sat 2024-08-03  Sat 2024-08-03  Kauhajoki P18            Pojat 18
|               |               |                        |
Sat 2024-08-10  Sat 2024-08-10  Tampere                  JNBT miehet
Sat 2024-08-10  Sun 2024-08-11  Tampere Finaalit P18     Pojat 18
|               |               |                        |
Sat 2024-08-24  Sat 2024-08-24  Finaalit Hietsu          JNBT miehet
(venv) $
````
