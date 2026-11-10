# Leader compatibility

The inventory includes every playable leader/civilization pair exposed by the pinned Gathering Storm configuration snapshot, including alternate personas and leaders shared by two civilizations. Classic+ does not change selection rows. All entries are **runtime unverified**. Owners of fewer DLC packs will see fewer entries.

## M1 changes to check

| Leaders or civilization | Removed dependency | Preview behavior |
| --- | --- | --- |
| Abraham Lincoln and both Teddy Roosevelt personas / America | Wildcard slots generated Favor | Wildcard conversion remains; +1 Influence Point per turn. |
| Wilfrid Laurier / Canada | Tourism generated Favor; extra emergency rewards | Retains its peace restrictions; trade routes to city-states gain +2 Culture. |
| Kristina / Sweden | Recruiting Great People generated Favor; Nobel competitions | Factory and University Great Person points and Kristina's theming remain. |
| Lautaro / Mapuche | Bonus against Golden Age rivals, extra age-based loyalty loss | +10 strength against Free Cities; ordinary loyalty loss from kills and existing governor effects remain. |
| Mansa Musa / Mali | Trade capacity gained through Golden Ages | +1 trade route at Political Philosophy, with desert trade yields unchanged. |
| Magnificent Suleiman / Ottomans | Alternating age-dependent yields and combat | +5% Science and Culture and +2 combat strength, regardless of age. |
| Tamar / Georgia | Golden Age dedications and Tsikhe age bonuses | Wall production, envoy and faith-from-kills abilities remain; Tsikhe gains +2 steady Faith and +1 additional Tourism after Conservation. |

Seondeok and original Suleiman still rely on governors; the M2 preview has not started. Global systems and unique-content interactions (e.g. Országház for any builder, or Greece's shared diplomatic infrastructure) require separate checks.

## Complete snapshot inventory

Candidate flags below come from scanning leader/civilization traits, unique content, attached modifiers and requirement identifiers, and XP2 resource and power fields. They are review leads, not proven dependencies: an identifier can mention a system without depending on it. “None flagged” is not a pass and does not clear hard-coded effects, agendas, descriptions, or indirect dependencies. The above M1 changes have been checked at the database level only.

| Leader | Civilization | Candidate flags before Classic+ |
| --- | --- | --- |
| `LEADER_ABRAHAM_LINCOLN` | `CIVILIZATION_AMERICA` | Congress, Resources, Power |
| `LEADER_ALEXANDER` | `CIVILIZATION_MACEDON` | Resources |
| `LEADER_AMANITORE` | `CIVILIZATION_NUBIA` | None flagged |
| `LEADER_AMBIORIX` | `CIVILIZATION_GAUL` | None flagged |
| `LEADER_BARBAROSSA` | `CIVILIZATION_GERMANY` | None flagged |
| `LEADER_BASIL` | `CIVILIZATION_BYZANTIUM` | Resources |
| `LEADER_CATHERINE_DE_MEDICI` | `CIVILIZATION_FRANCE` | Resources |
| `LEADER_CATHERINE_DE_MEDICI_ALT` | `CIVILIZATION_FRANCE` | Resources |
| `LEADER_CHANDRAGUPTA` | `CIVILIZATION_INDIA` | None flagged |
| `LEADER_CLEOPATRA` | `CIVILIZATION_EGYPT` | None flagged |
| `LEADER_CLEOPATRA_ALT` | `CIVILIZATION_EGYPT` | None flagged |
| `LEADER_CYRUS` | `CIVILIZATION_PERSIA` | Resources, Grievances |
| `LEADER_DIDO` | `CIVILIZATION_PHOENICIA` | None flagged |
| `LEADER_ELEANOR_ENGLAND` | `CIVILIZATION_ENGLAND` | Resources, Power |
| `LEADER_ELEANOR_FRANCE` | `CIVILIZATION_FRANCE` | Resources |
| `LEADER_ELIZABETH` | `CIVILIZATION_ENGLAND` | Resources, Power |
| `LEADER_GANDHI` | `CIVILIZATION_INDIA` | None flagged |
| `LEADER_GENGHIS_KHAN` | `CIVILIZATION_MONGOLIA` | Resources |
| `LEADER_GILGAMESH` | `CIVILIZATION_SUMERIA` | None flagged |
| `LEADER_GITARJA` | `CIVILIZATION_INDONESIA` | None flagged |
| `LEADER_GORGO` | `CIVILIZATION_GREECE` | None flagged |
| `LEADER_HAMMURABI` | `CIVILIZATION_BABYLON_STK` | None flagged |
| `LEADER_HARALD_ALT` | `CIVILIZATION_NORWAY` | Resources |
| `LEADER_HARDRADA` | `CIVILIZATION_NORWAY` | Resources |
| `LEADER_HOJO` | `CIVILIZATION_JAPAN` | Resources, Power |
| `LEADER_JADWIGA` | `CIVILIZATION_POLAND` | Resources |
| `LEADER_JAYAVARMAN` | `CIVILIZATION_KHMER` | None flagged |
| `LEADER_JOAO_III` | `CIVILIZATION_PORTUGAL` | None flagged |
| `LEADER_JOHN_CURTIN` | `CIVILIZATION_AUSTRALIA` | None flagged |
| `LEADER_JULIUS_CAESAR` | `CIVILIZATION_ROME` | Resources |
| `LEADER_KRISTINA` | `CIVILIZATION_SWEDEN` | Congress |
| `LEADER_KUBLAI_KHAN_CHINA` | `CIVILIZATION_CHINA` | None flagged |
| `LEADER_KUBLAI_KHAN_MONGOLIA` | `CIVILIZATION_MONGOLIA` | Resources |
| `LEADER_KUPE` | `CIVILIZATION_MAORI` | Resources |
| `LEADER_LADY_SIX_SKY` | `CIVILIZATION_MAYA` | None flagged |
| `LEADER_LADY_TRIEU` | `CIVILIZATION_VIETNAM` | None flagged |
| `LEADER_LAURIER` | `CIVILIZATION_CANADA` | Congress, Resources |
| `LEADER_LAUTARO` | `CIVILIZATION_MAPUCHE` | Ages, Governors |
| `LEADER_LUDWIG` | `CIVILIZATION_GERMANY` | None flagged |
| `LEADER_MANSA_MUSA` | `CIVILIZATION_MALI` | Ages, Resources |
| `LEADER_MATTHIAS_CORVINUS` | `CIVILIZATION_HUNGARY` | Resources |
| `LEADER_MENELIK` | `CIVILIZATION_ETHIOPIA` | Resources |
| `LEADER_MONTEZUMA` | `CIVILIZATION_AZTEC` | None flagged |
| `LEADER_MVEMBA` | `CIVILIZATION_KONGO` | Resources |
| `LEADER_NADER_SHAH` | `CIVILIZATION_PERSIA` | Resources |
| `LEADER_NZINGA_MBANDE` | `CIVILIZATION_KONGO` | Resources |
| `LEADER_PACHACUTI` | `CIVILIZATION_INCA` | None flagged |
| `LEADER_PEDRO` | `CIVILIZATION_BRAZIL` | Resources |
| `LEADER_PERICLES` | `CIVILIZATION_GREECE` | Congress |
| `LEADER_PETER_GREAT` | `CIVILIZATION_RUSSIA` | Resources |
| `LEADER_PHILIP_II` | `CIVILIZATION_SPAIN` | Resources |
| `LEADER_POUNDMAKER` | `CIVILIZATION_CREE` | None flagged |
| `LEADER_QIN` | `CIVILIZATION_CHINA` | None flagged |
| `LEADER_QIN_ALT` | `CIVILIZATION_CHINA` | None flagged |
| `LEADER_RAMSES` | `CIVILIZATION_EGYPT` | None flagged |
| `LEADER_ROBERT_THE_BRUCE` | `CIVILIZATION_SCOTLAND` | None flagged |
| `LEADER_SALADIN` | `CIVILIZATION_ARABIA` | Resources |
| `LEADER_SALADIN_ALT` | `CIVILIZATION_ARABIA` | Resources |
| `LEADER_SEJONG` | `CIVILIZATION_KOREA` | Power |
| `LEADER_SEONDEOK` | `CIVILIZATION_KOREA` | Governors |
| `LEADER_SHAKA` | `CIVILIZATION_ZULU` | None flagged |
| `LEADER_SIMON_BOLIVAR` | `CIVILIZATION_GRAN_COLOMBIA` | Resources |
| `LEADER_SULEIMAN` | `CIVILIZATION_OTTOMAN` | Governors, Resources |
| `LEADER_SULEIMAN_ALT` | `CIVILIZATION_OTTOMAN` | Ages, Resources |
| `LEADER_SUNDIATA_KEITA` | `CIVILIZATION_MALI` | Resources |
| `LEADER_TAMAR` | `CIVILIZATION_GEORGIA` | Ages, Congress, Resources |
| `LEADER_THEODORA` | `CIVILIZATION_BYZANTIUM` | None flagged |
| `LEADER_TOKUGAWA` | `CIVILIZATION_JAPAN` | Resources, Power |
| `LEADER_TOMYRIS` | `CIVILIZATION_SCYTHIA` | None flagged |
| `LEADER_TRAJAN` | `CIVILIZATION_ROME` | Resources |
| `LEADER_T_ROOSEVELT` | `CIVILIZATION_AMERICA` | Congress, Resources, Power |
| `LEADER_T_ROOSEVELT_ROUGHRIDER` | `CIVILIZATION_AMERICA` | Congress, Resources, Power |
| `LEADER_VICTORIA` | `CIVILIZATION_ENGLAND` | Resources, Power |
| `LEADER_VICTORIA_ALT` | `CIVILIZATION_ENGLAND` | Resources, Power |
| `LEADER_WILHELMINA` | `CIVILIZATION_NETHERLANDS` | Resources |
| `LEADER_WU_ZETIAN` | `CIVILIZATION_CHINA` | None flagged |
| `LEADER_YONGLE` | `CIVILIZATION_CHINA` | None flagged |

77 playable entries.
