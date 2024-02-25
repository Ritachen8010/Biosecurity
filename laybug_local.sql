-- create database
CREATE DATABASE `ladybug`;
SHOW DATABASES;
DROP DATABASE `ladybug`; -- DO NOT PUSH

-- create table
USE `ladybug`;

-- show table
DESCRIBE `agro`;

-- quarry 
SELECT * FROM `user`;
SELECT * FROM `agro`;
SELECT * FROM `staff_admin`;
SELECT * FROM `guide_info`;
SELECT * FROM `image`;


-- create user table - manager user
CREATE TABLE `user`(
	`user_id` INT AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(50) NOT NULL UNIQUE,
    `role` ENUM ('agronomist', 'staff', 'admin') NOT NULL,
    `status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    PRIMARY KEY (`user_id`)
)ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- insert data - user
INSERT INTO `user` (`username`, `password`, `email`, `role`, `status`)
VALUES
('cindyyang', 'password123', 'cindy.yang@example.com', 'agronomist', 'active'),
('jennywang', 'password123', 'jenny.wang@example.com', 'agronomist', 'active'),
('lilili', 'password123', 'lili.li@example.com', 'agronomist', 'active'),
('harryporter', 'password123', 'harry.porter@example.com', 'agronomist', 'active'),
('pinapple123', 'password123', 'pinapple.blueberry@example.com', 'agronomist', 'active');

-- insert data - staff
INSERT INTO `user` (`user_id`, `username`, `password`, `email`, `role`, `status`)
VALUES
('1', 'rita123', 'password123', 'rita.chen@example.com', 'admin', 'active'),
('2', 'lyn123', 'password123', 'lyn.jin@example.com', 'staff', 'active'),
('3', 'lana1124', 'password123', 'lana.su@example.com', 'staff', 'active'),
('4', 'fye1156', 'password123', 'fye.xiang@example.com', 'staff', 'active');

-- create agro table
CREATE TABLE `agro`(
	`agro_id` INT NOT NULL UNIQUE AUTO_INCREMENT,
    `user_id` INT,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `address` VARCHAR(100),
    `phone_num` VARCHAR(20),
    `date_joined` DATE,
    PRIMARY KEY (`agro_id`),
	FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
);

-- insert data - agro
INSERT INTO `agro` (`user_id`, `first_name`, `last_name`, `address`, `phone_num`, `date_joined`)
VALUES
(26, 'Cindy', 'Yang', '123 Main St, Anytown', '021-12345678', '2013-06-05'),
(27, 'Jenny', 'Wang', '68 One St, Anytown', '021-88866601', '2018-08-12'),
(28, 'Lili', 'LI', '3 Small St, Anytown', '021-45622310', '2001-02-12'),
(29, 'Harry', 'Porter', '4 Privet St, Anytown', '021-55562317', '2011-01-30'),
(30, 'Liam', 'William', '99 Sea St, Anytown', '021-42215618', '2011-01-30');

-- create staff_admin table
CREATE TABLE `staff_admin`(
	`staff_id` INT NOT NULL UNIQUE AUTO_INCREMENT,
    `user_id` INT,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `work_phone_num` VARCHAR(20),
    `hire_date` DATE,
    `pos` VARCHAR(50),
    `dept` VARCHAR(50),
    `status` ENUM ('active', 'inactive'),
    PRIMARY KEY (`staff_id`),
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
);

-- insert data - staff_admin
INSERT INTO `staff_admin` (`user_id`, `first_name`, `last_name`, `work_phone_num`, `hire_date`, `pos`, `dept`, `status`)
VALUES
(1, 'Rita', 'Chen', '021-65432109', '2020-08-10', 'admin', 'Management', 'active'),
(2, 'Lyn', 'Jin', '021-76998035', '2010-04-10', 'staff', 'Management', 'active'),
(3, 'Lana', 'Su', '021-76774356', '2023-07-10', 'staff', 'IT', 'active'),
(4, 'Fye', 'Xiang', '021-12338857', '2015-06-10', 'staff', 'IT', 'active');

-- create guide table
CREATE TABLE `guide_info`(
	`guide_id` INT AUTO_INCREMENT,
    `item_type` ENUM ('pest', 'weed'),
    `name` VARCHAR(100) NOT NULL,
    `common_name` VARCHAR(100),
    `key_char` TEXT,
    `bio` TEXT,
    `impact` TEXT,
    `control` TEXT,
    `further_info` TEXT,
    PRIMARY KEY (`guide_id`)
);

-- insert data - guide info - pest

-- 1
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Listronotus bonariensis', 'Argentine stem weevil adult', 
-- key_char
'• Argentine stem weevil is common throughout New Zealand.
\n• Adults are small (2-3 mm long) and cryptically coloured making them difficult to see.
\n• Black elongated eggs are laid singularly or in groups of 2-4 in the leaf sheath of grasses.
\n• On hatching the white legless larvae tunnel into the grass stem where they usually remain until ready to pupate.
\n• Larvae pass through five stages increasing in size as they do. Larvae in the 5th stage may live outside of the plant particularly if the grass tillers are small.
\n• Pupation occurs in the litter layer.',
-- bio
'• Argentine stem weevil (Listronotus bonariensis), an exotic weevil of South American origin, is ubiquitous in agricultural and amenity turf environments throughout the country. It used to be rated New Zealand’s worst insect pest of pasture.
\n• With the sucessful introduction of a biocontrol agent and development of endophyte infected ryegrasses, Argentine stem weevil, although still a major pest, no longer has the impact it once had.
\n• The adults feed on a range of grasses but it is the larvae which develop and feed, predominantly, within the tillers of several agriculturally important grasses that are the main pest stage. These weevils are a major pest of perennial ryegrass (Lolium perenne) in developed pastures, maize and cereal crops. Uncontrolled they have been estimated to cost the country up to $280m per annum.
\n• The adult weevil is a hard bodied compact beetle usually less than 3.5 mm long and 1.5 mm wide. It is grey-brown with three pale longitudinal stripes on its thorax. Its colour, small size and the fact that soil particles adhere to its body make adult weevils very difficult to detect by eye.
\n• Although it can be active during daylight, night is when it usually feeds on the leaf blades and lay its eggs. Adult weevils commence egg laying in spring as soon as temperatures allow (average daily temp 10°C).
\n• Eggs are laid in the sheaths of grass tillers. After hatching the white legless larvae tunnel and feed within tillers. Large larvae may live outside the tillers and within the plant crown especially if the tillers are small. Each larvae may destroy up to eight ryegrass tillers during development to adult and are capable of moving to new plants when required. The larvae pass through five stages of development before leaving the plants and pupating in soil.
\n• New adults commence laying eggs almost immediately after emergence from pupae giving rise to a new generation but egg laying is controlled by day-length and stops in Mid-March.
\n• The number of generations Argentine stem weevil can achieve in a year is driven by temperature. Pest status is reached when two or more generations occur as happens from Canterbury northwards. In Otago and Southland historically only one generation has generally occurred each year but anecdotal evidence suggests this has changed and stem weevil may be increasing in significance.
\n• The adult weevils can fly and mass dispersal flights can take place on calm, sunny days in summer and autumn.
\n• Grasses, especially Italian and endophyte-free perennial ryegrasses, seedling maize and cereals, are the main hosts. Adults have been reported feeding on germinating brassica crops but may easily be mistaken for native weevils which commonly do this.',
-- impact
'• Adult feeding is characterised by “windowing” of the grass leaf near its tip. Windows are typically rectangular and appear as clear areas, the pane being the lower leaf cuticle which is left intact. Veins encountered while the adults feed are cut at the base and displaced. They appear as pigtail-like threads attached at the upper edge of the window.
\n• Adult feeding damage is not normally significant except in summer-sown pasture. Larvae mining the stem do the greatest damage to vegetative tillers, which wilt and yellow from the centre outwards. Damaged tillers contain larval frass and may show small, circular exit holes near the base. Flowering tillers when attacked whiten and may snap off owing to mechanical weakening. Where infestation is heavy, severe damage is done to the sward, particularly in dry conditions when pasture growth is retarded.
\n• The presence of an endophytic fungus in perennial ryegrass makes it less susceptible to Argentine stem weevil attack. Endophytes do not occur in annual ryegrasses.
\n• Other pasture grasses, cereals and maize are are also affected by argentine stem weevil. They are often reported feeding on other plants e.g. brassica seedlings. In such instances this may be driven by shortage of grasses for food or the weevils may be seeking moisture.
\n• Several species of native weevils that appear superficially similar to Argentine stem weevil are common in some pastures and crops and these are easily mistaken for Argentine stem weevil. It is quite likely that most damage to non-grass crops attributed to stem weevil is due to native weevil feeding.',
-- control
'• Argentine stem weevil is difficult to control with insecticides. Several products are available that will kill adult weevils but pastures can be rapidly re-infested from others nearby. The larvae generally live within the plants on which they feed and are therefore protected from most insecticides.
\n• When establishing new pastures there are some options that can mitigate damage from this pest. Cultivation can destroy larval weevil populations and allow re-establishment of grasses into a clean pasture. This however will not protect against adults which may survive cultivation or re-invade the paddock. An insecticide can be used if necessary in this situation. Foliar sprays, prills drilled with the seed and seed coatings are available.
\n• If very high numbers of adults are present insecticide seed coating may not offer sufficient protection to avoid loss of seedlings. Even endophyte infected seedlings (see below) are vulnerable to attack while establishing.
\n• If direct-drilling is used to re-establish pastures larvae are able to survive in dying vegetation and migrate to new plants after sowing. As with all insect pests assessing the probability of damage will assist in choosing a control option.
\n• A small wasp, Microctonus hyperodae, was introduced to New Zealand in 1990 as a biological control agent and was released throughout the country. It is now well established in most areas and in combination with endophyte infected ryegrasses has reduced the impact this weevil formerly had on New Zealand pastures. This wasp is a parasite and lays its eggs inside the adult weevil. This sterilises and eventually kills the weevil.
\n• Endophyte is a term used to describe an organism that lives inside another. In this case the endophyte is a fungus called Neotyphodium lolii that lives within perennial ryegrass plants.
\n• Toxins produced by this fungus protect the plant from grazing. The “wild type” endophyte that can occur naturally in ryegrass, and used to be common in pasture cultivars, protected the plants from argentine stem weevil but was also responsible for stock health problems such as heat stress and ryegrass staggers.
\n• Plant breeders have been able to selectively improve the fungus and ryegrass cultivars are now available with a choice of endophyte. The most prominent of these is called AR1, but NEA2 in Trojan and AR37 are also effective. These forms of the endophyte protect ryegrass from argentine stem weevil but eliminate or reduce the effects on stock caused by the standard endophyte. When selecting perennial ryegrass cultivars for pastures, one of these endophytes should generally be used and form the backbone of argentine stem weevil management. AR37 and NEA2 in Trojan will also protect against other insect pests.',
-- further info
'• Choosing a ryegrass endophyte: https://live-agpest.pantheonsite.io/wp-content/uploads/2013/06/Endophyte-Table-2013.pdf');

-- 2
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Prietocella barbara', 'Banded Conical Snail',
-- key_char
'• Currently found in Northland, Auckland and Waikato with one record from Poverty Bay.
\n• Pest of plantain, chicory, brassica, maize and grain crops.
\n• Will also feed on lettuce, broccoli, cabbage and silverbeet.
\n• Often found on clover but does not eat clover.
\n• The pointed shells can be up to 7 mm.
\n• Shell colour ranges from off-white to grey to pale yellow. Darker patterning, spots, or stripes may also be present.',
-- bio
'• Banded conical snail originated in the Mediterranean but has spread to several countries.
\n• First recorded in 1983 in New Zealand, it is now commonly found in Northland, Auckland and Waikato but only once elsewhere and that is in Poverty Bay. However, its distribution may be greater that this and is likely to expand.
\n• There appears to be two generations per year. Few snails are found in mid-summer but this may be due migration from crops and pastures to roadsides or other sheltered aestivation sites. Eggs appear to be laid in spring and again in late summer early autumn.',
-- impact
'• Banded conical snail appears to have a wide food range but has only been recorded damaging plantain, chicory and cabbages in New Zealand. It will feed on dead plant material, lettuce, broccoli and silver beet suggesting other field crops (brassicas and fodder beet) may also host populations. The main impact on plantain and chicory crops is noticed around October when snail numbers are high and they are feeding voraciously.
\n• Established and seedling crops are attacked. Damage appears as small “shot” holes in leaves.
\n• In Australia they have been recorded damaging cereal seedlings and in summer collect in the stalks of cereals and maize clogging machinery during harvest.
\n• It is possible that banded conical snail could be a vector for lung worm in New Zealand but this is not proven.
\n• Although it is often seen on clover, banded conical snail has not been shown to feed on clover.',
-- control
'There are no established control technologies in New Zealand. In Australia trials investigating standard molluscicide baits have given variable results with the explanation that although all the standard active ingredients are toxic to the snails, banded conical snail adults are not attracted to the baits only encountering and feeding on them by chance, while immature snails don’t appear to feed on the baits.
\nWeed control can reduce the number of snails infesting crops.
\nStubble management and the presence of large amounts of organic matter also have variable effects on subsequent seedling crop damage. Stubble burning reduces snail numbers markedly.',
-- further info
'• jennydymock@ihug.co.nz');

-- 3
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Heteronychus arator', 'Black beetle adult',
-- key_char
'• Black beetle is a pest in northern North Island.
\n• Warm years favour black beetle populations.
\n• Both beetles and larvae damage pasture, other agricultural and some horticultural crops.
\n• Larvae cause damage to pasture in summer.
\n• Adult beetles cause damage in autumn and spring.',
-- bio
'• Black beetle is an African species but has been present in New Zealand for several decades. It is at the limit of its climatic tolerance and is restricted to Waikato and Bay of Plenty northwards with a southward coastal extension into northern Taranaki and Gisborne. Black beetle outbreaks occur sporadically and follow above average spring temperatures. It has a high temperature requirement for most life processes. Female longevity, number of eggs produced, egg viability, larval survival, growth rate and the amount they eat are all favoured by temperatures greater than 20°C and are severely inhibited at between 10-15°C.
\n• Adult beetles are a characteristic glossy black and about 15 mm long with females being larger than males. They are usually found in the top 1 cm of soil. They undergo extensive dispersal flights in spring and autumn but surface air temperatures must be above 17°C for flights to occur. The eggs, about 2 mm long and ovoid to spherical in shape, are laid singly in soil, close to the surface, in spring.
\n• The creamy white C shaped larvae, usually found in the top 10 cm of soil, appear superficially like common grass-grub but are larger reaching 2.5 cm when fully grown. These fully grown larave are present and cause damage in summer. In black beetle areas any grass-grub larvae present will be very small (less than 10 mm) at the same time of year. Black beetle larvae can also be distinguished from grass-grub by breathing pores (spiracles) that occur down the length of the body. In grass-grub these are not obvious but in black beetle they are prominent and show clearly as orange spots. Like grass-grub the larvae pass through 3 stages before pupating and emerging as adults. Pupation occurs in February/March and the beetles overwinter. These beetles will not lay eggs until the following spring.',
-- impact
'• The beetles and larvae of black beetle feed on several pasture grasses including annual ryegrasses, perennial ryegrasses, tall fescue, paspalum and kikuyu. Grasses with high carbohydrate levels in their roots favour adult development and ultimately the size of the populations that develop.
\n• larval feeding is on roots often close to the surface. In severe infestations the turf can be rolled back owing to the destruction of the root system. In less severe cases the pastures can become clover dominated as legumes are not a favoured food source, or they can become open and susceptible to weed invasion. Damage to pastures from larvae can appear similar to common grass-grub but occurs over summer (January to March) as opposed to autumn/winter. The damage threshold for black beetle larvae is approximately 20-30/m2 which is considerably lower than for grass-grub.
\n• Patches of yellowing tillers that pull easily from the pasture may become noticeable in autumn and spring. This is a sign of adult feeding. Adults may feed on roots or on the base of plants at soil level. Any more than 10 adults/m2 in pasture are a concern but populations of 30/m2 have become common and they can reach as high as 95/m2. In maize 1-2 beetles/m2 in spring are sufficient to cause an economic loss.
\n• Both larvae and adults can be particularly destructive to newly sown grasses.
\n• Beetles and larvae will also feed on brassica roots, maize, sweetcorn, kumara and strawberries. A series of dry summers and autumns since 2007/8 has contributed to higher than usual numbers of black beetle particularly on light soil types.
\n• Pugging as a result of plant destruction can be a serious issue.
\n• Damage is generally more severe on dairy than on sheep and beef farms but occurs on all types.',
-- control
'• There are few control options available for black beetle other than sowing resistant grasses. Ryegrasses containing the AR37 endophyte are the best option in black beetle prone areas but some protection will also be gained using Endo 5 or NEA2.  Wild type (or standard endophyte) also protects from black beetle feeding. Max P in tall fescue helps protect that grass.These endophyte fungi produce toxins that deter the adult black beetles from feeding and if the beetles cannot find alternative plants to feed on they will die before they can lay their eggs. The endophytes do not directly affect the larvae. AR1 infected ryegrasses ARE NOT protected from black beetle feeding. For endophyte selection see http://www.dairynz.co.nz/page/pageid/2145866515/Pasture.
\n• Grass type can affect beetle development. Grasses with high root levels of carbohydrate enable faster beetle maturation. These include paspalum, kikuyu and several other weed grasses. Eliminating these grasses from pasture will slow development and reduce the problem. Annual ryegrasses are good host plants for black beetle.
\n• No chemicals are registered for control of larvae or adults in pasture. Imidacloprid is available as a seed coating.
\n• Sowing insecticide treated seed can provide protection against adult beeles and assist seedling establishment. It will not protect against larvae and if beetle flights are prolonged the level of protection offered may not be enough. Sowing should be delayed until late February to avoid larval attack. To maximise the benefits of pasture renovation and of the endophyte containing grasses it is important that seed is sown into clean paddocks free of other grasses that the beetles can feed on. Any pasture renewal planned for autumn should be consistent with best practice guidelines, see: http://www.dairynz.co.nz/file/fileid/34881.
\n• The use of a break crop that is unfavourable to black beetle can provide a clean seed bed and aid establishment of new pasture. Brassicas, maize, legumes and chicory do not support full development of black beetle and can be used in pasture renovation programmes.',
-- further info
'• Choosing a ryegrass endophyte: https://live-agpest.pantheonsite.io/wp-content/uploads/2013/06/Endophyte-Table-2013.pdf
\n• AgResearch: black beetle: https://www.agresearch.co.nz/our-science/biocontrol-biosecurity/pest-control/black-beetle/Pages/default.aspx.avg
DairyNZ: black beetle: https://www.dairynz.co.nz/blackbeetle/');

-- 4
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Heteronychus arator', 'Black beetle larvae',
-- key_char
'• Black beetle is a pest in northern North Island.
\n• Warm years favour black beetle populations.
\n• Both beetles and larvae damage pasture, other agricultural and some horticultural crops.
\n• Larvae cause damage to pasture in summer.
\n• Adult beetles cause damage in autumn and spring.',
-- bio
'• Black beetle is an African species but has been present in New Zealand for several decades. It is at the limit of its climatic tolerance and is restricted to Waikato and Bay of Plenty northwards with a southward coastal extension into northern Taranaki and Gisborne. Black beetle outbreaks occur sporadically and follow above average spring temperatures. It has a high temperature requirement for most life processes. Female longevity, number of eggs produced, egg viability, larval survival, growth rate and the amount they eat are all favoured by temperatures greater than 20°C and are severely inhibited at between 10-15°C.
\n• Adult beetles are a characteristic glossy black and about 15 mm long with females being larger than males. They are usually found in the top 1 cm of soil. They undergo extensive dispersal flights in spring and autumn but surface air temperatures must be above 17°C for flights to occur. The eggs, about 2 mm long and ovoid to spherical in shape, are laid singly in soil, close to the surface, in spring.
\n• The creamy white C shaped larvae, usually found in the top 10 cm of soil, appear superficially like common grass-grub but are larger reaching 2.5 cm when fully grown. These fully grown larave are present and cause damage in summer. In black beetle areas any grass-grub larvae present will be very small (less than 10 mm) at the same time of year. Black beetle larvae can also be distinguished from grass-grub by breathing pores (spiracles) that occur down the length of the body. In grass-grub these are not obvious but in black beetle they are prominent and show clearly as orange spots. Like grass-grub the larvae pass through 3 stages before pupating and emerging as adults. Pupation occurs in February/March and the beetles overwinter. These beetles will not lay eggs until the following spring.',
-- impact
'• The beetles and larvae of black beetle feed on several pasture grasses including annual ryegrasses, perennial ryegrasses, tall fescue, paspalum and kikuyu. Grasses with high carbohydrate levels in their roots favour adult development and ultimately the size of the populations that develop.
\n• larval feeding is on roots often close to the surface. In severe infestations the turf can be rolled back owing to the destruction of the root system. In less severe cases the pastures can become clover dominated as legumes are not a favoured food source, or they can become open and susceptible to weed invasion. Damage to pastures from larvae can appear similar to common grass-grub but occurs over summer (January to March) as opposed to autumn/winter. The damage threshold for black beetle larvae is approximately 20-30/m2 which is considerably lower than for grass-grub.
\n• Patches of yellowing tillers that pull easily from the pasture may become noticeable in autumn and spring. This is a sign of adult feeding. Adults may feed on roots or on the base of plants at soil level. Any more than 10 adults/m2 in pasture are a concern but populations of 30/m2 have become common and they can reach as high as 95/m2. In maize 1-2 beetles/m2 in spring are sufficient to cause an economic loss.
\n• Both larvae and adults can be particularly destructive to newly sown grasses.
\n• Beetles and larvae will also feed on brassica roots, maize, sweetcorn, kumara and strawberries. A series of dry summers and autumns since 2007/8 has contributed to higher than usual numbers of black beetle particularly on light soil types.
\n• Pugging as a result of plant destruction can be a serious issue.
\n• Damage is generally more severe on dairy than on sheep and beef farms but occurs on all types.',
-- control
'• There are few control options available for black beetle other than sowing resistant grasses. Ryegrasses containing the AR37 endophyte are the best option in black beetle prone areas but some protection will also be gained using Endo 5 or NEA2.  Wild type (or standard endophyte) also protects from black beetle feeding. Max P in tall fescue helps protect that grass.These endophyte fungi produce toxins that deter the adult black beetles from feeding and if the beetles cannot find alternative plants to feed on they will die before they can lay their eggs. The endophytes do not directly affect the larvae. AR1 infected ryegrasses ARE NOT protected from black beetle feeding. For endophyte selection see http://www.dairynz.co.nz/page/pageid/2145866515/Pasture.
\n• Grass type can affect beetle development. Grasses with high root levels of carbohydrate enable faster beetle maturation. These include paspalum, kikuyu and several other weed grasses. Eliminating these grasses from pasture will slow development and reduce the problem. Annual ryegrasses are good host plants for black beetle.
\n• No chemicals are registered for control of larvae or adults in pasture. Imidacloprid is available as a seed coating.
\n• Sowing insecticide treated seed can provide protection against adult beeles and assist seedling establishment. It will not protect against larvae and if beetle flights are prolonged the level of protection offered may not be enough. Sowing should be delayed until late February to avoid larval attack. To maximise the benefits of pasture renovation and of the endophyte containing grasses it is important that seed is sown into clean paddocks free of other grasses that the beetles can feed on. Any pasture renewal planned for autumn should be consistent with best practice guidelines, see: http://www.dairynz.co.nz/file/fileid/34881.
\n• The use of a break crop that is unfavourable to black beetle can provide a clean seed bed and aid establishment of new pasture. Brassicas, maize, legumes and chicory do not support full development of black beetle and can be used in pasture renovation programmes.',
-- further info
'• Choosing a ryegrass endophyte: https://live-agpest.pantheonsite.io/wp-content/uploads/2013/06/Endophyte-Table-2013.pdf
\n• AgResearch: black beetle: https://www.agresearch.co.nz/our-science/biocontrol-biosecurity/pest-control/black-beetle/Pages/default.aspx.avg
DairyNZ: black beetle: https://www.dairynz.co.nz/blackbeetle/');

-- 5
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Sminthurus viridis', 'Clover flea, clover springtail, lucerne flea',
-- key_char
'• Found throughout New Zealand.
\n• Usually only a pest in Northland, South Auckland, Waikato and the Bay of Plenty.
\n• Small (>1 mm) yellow/green insects that jump when disturbed.
\n• Clover flea will feed on a range of legumes but white clover is the preferred food plant.
\n• Damage can also be caused to lucerne, subterranean clover and when numbers are very high to grasses.
\n• Damage is caused primarily in spring and autumn.',
-- bio
'• Clover flea is a misleading term as they are not fleas at all and indeed may not even be insects. They are a type of Collembola commonly known as globular springtails. This name derives from them appearing to consist of 2 attached balls (hence globular) and a specialised appendage which enables them to spring very quickly into the air (hence springtail and flea). The same animal is also known as lucerne flea. Clover flea is present throughout New Zealand only reaching pest status in localised areas of the North Island – dairy pastures in parts of Northland, South Auckland, Waikato and the Bay of Plenty.
\n• After mating female clover fleas lay their eggs in batches of 2 – 40. These usually hatch after 26 – 42 days depending on temperature. Eggs laid in late spring take longer to hatch and will not do so until they have undergone periods of dry conditions followed by declining soil temperatures and increasing soil temperatures. This avoids the eggs hatching during dry summer months when food may be scarce. After hatching the young clover flea passes through 7 moults increasing in size each time until they reach a maximum size of about 3mm. Females tend to be larger than males but both are yellow green in colour with brown mottling on their backs. The adults live for approximately 15 days during which time males and females mate and egg laying starts again.',
-- impact
'• Clover flea is present throughout New Zealand but severe damage only occurs to dairy pastures in localised areas of the North Island – parts of Northland, South Auckland, Waikato and the Bay of Plenty.
\n• Clover flea will feed on a range of legumes but white clover is the preferred food plant in New Zealand. Damage can also be caused to lucerne, subterranean clover and when numbers are very high to grasses.
\n• Damage to clover results from young nymphs eating small holes in the leaves, giving the leaves a speckled appearance, while feeding from older nymphs and adults produces window like openings in the leaves. In cases of heavy infestation only the veins and cuticle of the clover leaf remain.
\n• Pasture damage is caused in late spring when high numbers of nymphs and adults can be present.
\n• Numbers of nymphs and adults are lower during summer, when mainly eggs are present, but increase again in autumn when again damage can occur.
\n• Pasture production losses of up to 20% frequently occur and reductions in clover yield of up to 50% have been recorded.
\n• Compounding direct feeding losses is that stock will avoid eating pasture fouled by clover flea faeces.',
-- control
'• Several insecticides are registered for use against clover flea (see below) and both spray and granular formulations can be successfully used. Applications should be applied when damage is first noticed or when high numbers of clover fleas are observed. At times repeat applications may be necessary to achieve good control. In this situation the most cost effective approach can be to use diflubenzuron in conjunction with another insecticide.
\n• Registered insecticides (active ingredients) for use against clover flea in pasture or clover seed crops are: chlorpyrifos, diazinon, diflubenzuron, dimethoate, fenitrothion and maldison.
\n• Consult your farm consultant, industry rep or the New Zealand Agricultural Manual for more information about chemical control.',
-- further_info
'NULL');

-- 6
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Agrotis ipsilon', 'Greasy cutworm',
-- key_char
'• Found throughout agricultural areas of New Zealand.
\n• Has a very wide host range including many vegetables, maize, sweetcorn, cereals, grasses, lucerne, white clover, plantain, and weeds such as docks.
\n• Although generally considered a minor pest, it can be a serious problem in kumara and seedling maize and sweetcorn field crops.
\n• The moths are nocturnal and attracted to lights. They are dark mottled brown to greyish-brown, with females darker than males. At rest they have a rectangular shape and are 35- 50 mm long.
\n• Eggs are laid singly or in clusters on vegetation, plant debris or into cracks in the ground, with low, dense vegetation (e.g. broadleaved weeds) being preferred.
\n• Small caterpillars are reddish brown to greyish green and are usually found on plant foliage.
\n• Larger caterpillars live in burrows up to 8 cm deep in the soil. They are typically greyish-green with two yellowish longitudinal stripes down the body. Their skin has a shiny greasy appearance.',
-- bio
'• Moths can be found year round but are most common from October to April. Most greasy cutworm overwinter as larvae and pupae. Caterpillars can also be found throughout the year but growth and development only occur when temperatures exceed 10.4oC.
\n• Each female moth lays around 600-800 eggs which initially are whitish-yellow but turn brown within 24 hours and become darker as hatching approaches. In summer they hatch in 3-7 days.
\n• After hatching young caterpillars forage on leaves until they are about one third grown. Larger caterpillars lie curled up 25-50mm below the soil surface during the day and emerge at night to feed. They often store parts of severed plants underground allowing them to remain underground for several days during unfavourable weather.
\n• The caterpillars can grow up to 50 mm long. When fully grown they form earthen cells in the top 50 mm of soil and pupate. Pupae are 17-25 mm long and reddish-brown appearing almost black just before the moth emerges.
\n• The normal summer life cycle takes from 7 to 12 weeks but varies in length depending on location and climate. There are 2-3 generations per year.',
-- impact
'• The larger caterpillars are the most damaging stage, cutting seedlings off at their base or tunnelling in the stems.
\n• Maize plants cut above the growing point usually survive but have greatly reduced yields.
\n• Losses of well over 10,000 plants/ha can occur at populations of 3 caterpillars/100 plants before the two leaf stage or 6 caterpillars/100 plants at the two to four leaf stage.
\n• Brassica seedlings and fodder beet seedlings can also be cut at ground level and killed. Feeding to cotyledons and leaves may slow plant growth.
\n• During windy periods eggs are usually laid on the leeward side of shelter (trees, hedges etc) resulting in damage often being worst in these areas.',
-- control
'• Thorough cultivation and good weed control, to eliminate alternative hosts (e.g. docks and plantains), before planting will reduce cutworm numbers.
\n• Sowing treated seed controls cutworms during seedling establishment, and also controls black beetle and stem weevil.
\n• Scout maize and sweetcorn paddocks regularly after maize emergence until the 4-leaf stage particularly on the leeward side of shelter. Where plants have been recently felled, scratching carefully in the soil around the cut plant base will usually reveal the curled up caterpillars. Their size will give an indication of future crop damage. Very large larvae about 50 mm long will be close to pupation and further feeding may be limited. Smaller larvae will feed for longer and continue to cause plant damage.
\n• A range of insecticides have registration for use against cutworm in maize. Synthetic pyrethroids are generally the most cost effective. In fields where cutworms are a perennial problem, an insecticide can be used in combination with pre-emergence herbicides to reduce cutworm numbers.
\n• Refer to the NZ Agrichemical manual or your local agrichemical representative for more information on insecticidal control.',
-- further_info
'Foundation for Arable Research Arable update No. 52. Greasy cutworm control in maize: https://www.far.org.nz/mm_uploads/52Mz_Cutworm.pdf');

-- 7
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Pieris brassicae', 'Great white butterfly',
-- key_char
'• Currently only found in Nelson where an eradication attempt is underway.
\n• Potential to spread throughout New Zealand.
\n• Pest of all brassica crops, and also found on nasturtiums.
\n• Butterflies look similar to cabbage white butterfly, but are 1.5 to 2 times bigger.
\n• Eggs are small and yellow, and are laid in clusters of 30-100 on top or bottom of leaf.
\n• Caterpillars have yellow and black markings, and feed together in clusters.',
-- bio
'• Discovered in Nelson in May 2010 and currently (December 2013) the target of an eradication attempt
\n• Adult butterflies are strong fliers, so could spread outside Nelson
\n• They fly on warm sunny days from early spring to late autumn
\n• Females lay eggs in batches of 30-100 on brassica leaves, and can lay up to 500 eggs in their lifetime
\n• Caterpillars feed in groups, often stripping all the leaves from a plant before dispersing to fresh plants
\n• Young small caterpillars are yellow with shiny black heads, then they develop black spots as they get older. Larger caterpillars are speckled grey-green and black with three yellow lines along their body and lots of pale hairs. Mature caterpillars are about 5 cm long
\n• Mature caterpillars crawl away from the plants and spin their cocoons in vertical surfaces such as walls, fences and tree trunks.
\n• In Nelson there are 3-4 generations per year.',
-- impact
'• Great white butterflies feed on all brassicas
\n• Feeding damage reduces yields and stock avoid grazing infested plants
\n• Scouting the crop will allow detection of eggs and caterpillars.',
-- control
'• Two insect biological control agents, the parasitic wasps Cotesia glomerata and Pteromalus puparum, attack great white butterfly in Nelson and should help to reduce its populations
\n• No insecticides are registered for use against giant white butterfly but those used against the common small white butterfly may provide control
\n• Great white butterfly should be reported to assist the eradication program
\n• Phone the Ministry for Primary Industries hotline 0800 80 99 66.',
-- further_info
'• Department of Conservation – Threats & Impacts: https://www.doc.govt.nz/conservation/threats-and-impacts/animal-pests/animal-pests-a-z/great-white-butterfly/
\n• Ministry for Primary Industries factsheet: https://www.mpi.govt.nz/files/pests/great-white-cabbage-butterfly-fact-sheet.pdf');

-- 8
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Adoryphorus coulonii', 'Redheaded pasture cockchafer',
-- key_char
'• Redheaded pasture cockchafer is currently restricted to pastures in some areas on the Port Hills and Banks Peninsula, Canterbury, and also to amenity turf within Christchurch city.
\n• This insect has a two-year lifecycle so serious damage may only occur once every two years.
\n• The very large larvae (up to 30 mm long) of this pest can cause serious pasture damage during autumn and winter.
\n• Adult beetles are not known to cause any damage.',
-- bio
'• The redheaded pasture cockchafer is an Australian species but has been present in Canterbury on the Port Hills and Banks Peninsula since the early 1960s. Only limited spread from the known infested areas has been observed to date. However, it is at serious pasture pest in Tasmania, South Australia, Victoria and parts of New South Wales and is possible it will eventually spread to pastures with similar characteristics in many areas of New Zealand.
\n• Adults are shiny dark brown/black robust looking beetles very similar in appearance to the African black beetle found in parts of the North Island. Both sexes are approximately 12 mm long and can be found close to the soil surface in pasture through early spring. The beetles undertake dispersal flights during warm evenings from September to mid-October. Eggs, about 2 mm long and ovoid to spherical in shape, are laid singly in soil 10 – 50mm deep in mid to late spring.
\n• The larvae pass through 3 stages during their first year before pupating and becoming beetles during the second summer of their two-year lifecycle. Beetles emerge from these pupae and spend the following autumn and winter deep in the soil before surfacing again as adult beetles in spring.
\n• The C shaped larvae appear superficially like common grass-grub but have a red head capsule and when full size, are up to four times the size and weight of a common grass grub.',
-- impact
'• Red headed pasture cockchafer larvae feed on organic matter and live root material present in the top 100 mm of soil.
\n• Pasture damage is caused by large 3rd stage larvae feeding on plant roots in autumn and winter. If large numbers of larvae are present pasture root systems can be completely severed about 2.5 cm below the soil surface and the pasture can be rolled up like a carpet. If lower numbers are present pasture damage similar to that caused by the New Zealand grass grub can appear with patches of dead pasture becoming visible and pulled plants seen post grazing.
\n• Shallow-rooted pasture plants are reported to be at most risk from cockchafer damage.
\n• The damage threshold for redheaded pasture cockchafer larvae, reported in Australian literature, is about 70/m2 which is considerably lower than for the New Zealand grass-grub.
\n• Beetles do not appear to feed so do not cause any damage.',
-- control
'• There are few options available to control the Australian redheaded pasture cockchafer.
\n• No chemicals are registered in New Zealand for control of larvae or adults in established pasture or for pasture seedling establishment.
\n• Off target use of insecticides registered for use against the common grass grub have been attempted with variable results. This pest prefers soils with high organic matter which may bind to insecticides and reduce their efficiency.
\n• Redheaded pasture cockchafer larvae are not known to be affected by any currently available grass endophytes. The adult beetle does not feed so is unlikely to be directly affected by endophytes.
\n• A biological control product based on a strain of the fungus Metarhizium anisopliae was developed and used in Australia in the 1990s but has since been removed from the market due to production problems.
\n• Reports from Australia suggest vigorous top-working, such as using a rototiller, greatly reduces damage to resown pastures.
\n• As this pest has a two-year lifecycle there may be a damaging population present in an area only each second year. Monitoring populations by spade sampling may allow a farmer to identify years in which new pastures could be established in the absence of potentially damaging populations.',
-- further_info
'• Agriculture Victoria Redheaded Pasture Cockchafer: https://agriculture.vic.gov.au/agriculture/pests-diseases-and-weeds/pest-insects-and-mites/the-redheaded-pasture-cockchafer 
\n• View the overlapping 2 year lifecycle of the Redheaded Pasture Cockchafer: https://live-agpest.pantheonsite.io/wp-content/uploads/2018/08/Redheaded-pasture-cockchafer-lifecycle.png');

-- 9
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Odontria striata (White)', 'Striped chafer adult',
-- key_char
'• Widespread native insect, most common in southern New Zealand, occasionally reaching pest levels.
\n• Feeds on a wide range of plants, larvae on roots and adults on foliage.
\n• Larvae are found in soil all year round.
\n• Adults are attracted to lights at night and can also be found in soil.
\n• Larvae appear very similar to common grass grub, but later stages are larger, and the head is usually darker.
\n• Commonly found in pasture.
\n• Often causes damage in home gardens.',
-- bio
'• Striped Chafer is found throughout New Zealand but most commonly in Canterbury, Otago and Southland.
\n• The approx. 14 mm long, dark brown, striped, velvety beetles of striped chafer are most often seen flying at dusk in spring and autumn although they can be found throughout the year.
\n• Spherical 1 to 1.5 mm dia. eggs are laid in the soil in batches of about 10-20 mainly from October until early February.
\n• The larvae pass through three stages and all three stages are present year round.
\n• Time spent as a larvae varies from 8-14 months.
\n• Pupation occurs in late summer early autumn.
\n• The eggs and larvae are generally found near the soil surface and large larvae may be surface active at least for short periods.
\n• The presence of large numbers of larvae is often indicated by large amounts of fine frass (very fine soil and organic particles) on the soil surface.
\n• Moist soils and lush vegetation are preferred by striped chafer and they cannot tolerate extremes of temperature or low soil moisture.',
-- impact
'• Striped chafer larvae feed on the roots of a wide range of plants including most pasture species.
\n• They occasionally cause damage to pasture and this tends to be on mid altitude country and predominantly in Otago and Southland.
\n• Low numbers of larvae occur in most southern pastures.
\n• When damaging levels of larvae are present pasture plants are easily pulled from the soil as a consequence of roots being destroyed. This is similar to common grass grub but striped chafer larvae aggregate less than grass grub so damage usually, but not exclusively, appears more widespread and less concentrated in patches.
\n• The larvae frequently cause damage to nursery and garden plants. Vegetable seedlings, root crops e.g. carrots and strawberries are frequently attacked.
\n• The beetles also feed on a wide range of plants including many pasture species, fruit trees and Eucalyptus species.
\n• The importance of adult feeding in pastures is unknown.
\n• When feeding on trees damage to young leaves is most likely to affect tree growth.',
-- control
'• There are no insecticides registered specifically for use against striped chafer but those used against the common grass grub are likely to also work against striped chafer larvae. However, Bioshield Grass GrubTM , a formulation of the bacterium Serratia entomophilla, is specific to common grass grub and will not control striped chafer.',
-- further_info
'• Barratt BIP, Campbell RA. 1982. Biology of the striped chafer, Odontria striata (Coleoptera: Scarabaeidae) l. The adult, flight and ground surface activity, female reproductive maturation, and food plant selection.  New Zealand Journal of Zoology, 1982, Vol. 9: 249-266.
\n• Barratt BIP, 1982. Biology of the striped chafer, Odontria striata (Coleoptera: Scarabaeidae) ll.Larval development.  New Zealand Journal of Zoology, 1982, Vol. 9: 267-278.');

-- 10
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('pest', 'Odontria striata (White)', 'Striped chafer larvae',
-- key_char
'• Widespread native insect, most common in southern New Zealand, occasionally reaching pest levels.
\n• Feeds on a wide range of plants, larvae on roots and adults on foliage.
\n• Larvae are found in soil all year round.
\n• Adults are attracted to lights at night and can also be found in soil.
\n• Larvae appear very similar to common grass grub, but later stages are larger, and the head is usually darker.
\n• Commonly found in pasture.
\n• Often causes damage in home gardens.',
-- bio
'• Striped Chafer is found throughout New Zealand but most commonly in Canterbury, Otago and Southland.
\n• The approx. 14 mm long, dark brown, striped, velvety beetles of striped chafer are most often seen flying at dusk in spring and autumn although they can be found throughout the year.
\n• Spherical 1 to 1.5 mm dia. eggs are laid in the soil in batches of about 10-20 mainly from October until early February.
\n• The larvae pass through three stages and all three stages are present year round.
\n• Time spent as a larvae varies from 8-14 months.
\n• Pupation occurs in late summer early autumn.
\n• The eggs and larvae are generally found near the soil surface and large larvae may be surface active at least for short periods.
\n• The presence of large numbers of larvae is often indicated by large amounts of fine frass (very fine soil and organic particles) on the soil surface.
\n• Moist soils and lush vegetation are preferred by striped chafer and they cannot tolerate extremes of temperature or low soil moisture.',
-- impact
'• Striped chafer larvae feed on the roots of a wide range of plants including most pasture species.
\n• They occasionally cause damage to pasture and this tends to be on mid altitude country and predominantly in Otago and Southland.
\n• Low numbers of larvae occur in most southern pastures.
\n• When damaging levels of larvae are present pasture plants are easily pulled from the soil as a consequence of roots being destroyed. This is similar to common grass grub but striped chafer larvae aggregate less than grass grub so damage usually, but not exclusively, appears more widespread and less concentrated in patches.
\n• The larvae frequently cause damage to nursery and garden plants. Vegetable seedlings, root crops e.g. carrots and strawberries are frequently attacked.
\n• The beetles also feed on a wide range of plants including many pasture species, fruit trees and Eucalyptus species.
\n• The importance of adult feeding in pastures is unknown.
\n• When feeding on trees damage to young leaves is most likely to affect tree growth.',
-- control
'• There are no insecticides registered specifically for use against striped chafer but those used against the common grass grub are likely to also work against striped chafer larvae. However, Bioshield Grass GrubTM , a formulation of the bacterium Serratia entomophilla, is specific to common grass grub and will not control striped chafer.',
-- further_info
'• Barratt BIP, Campbell RA. 1982. Biology of the striped chafer, Odontria striata (Coleoptera: Scarabaeidae) l. The adult, flight and ground surface activity, female reproductive maturation, and food plant selection.  New Zealand Journal of Zoology, 1982, Vol. 9: 249-266.
\n• Barratt BIP, 1982. Biology of the striped chafer, Odontria striata (Coleoptera: Scarabaeidae) ll.Larval development.  New Zealand Journal of Zoology, 1982, Vol. 9: 267-278.');

-- insert data - guide info - weed

-- 11
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Critesion spp', 'Barley grass',
-- key_char
'• Annual grass that germinates in autumn and sets seed in summer.
\n• Seeds have long bristly awns that stick to clothing and wool.
\n• Before plants flower they can be recognised by the slender but well-developed auricles that often encircle the base of the stem.
\n• Emerging leaves are rolled and leaves are often twisted.
\n• Leaves have a few hairs (unlike brome grasses which are very hairy).
\n• Ligule is short, white and irregularly toothed.',
-- bio
'• Originated in the Mediterranean, southwest Europe, and parts of Asia.
\n• Annual grass that mostly germinates in autumn and sets seed in summer.
\n• Germination can occur in spring and plants then produce seed late in a shortened growing season.
\n• Seeds have little dormancy and most germinate in the autumn following their production. A few can last longer if trapped under dry cow-pats or tree branches.
\n• Six species of barley grass are present in New Zealand: Critesion glaucum, C. hystrix, C. jubatum, C. marinum, C. murinum and C. secalinum. Differences between the six species are small and they can all be managed in the same way (i.e. same control methods).
\n• Barley grass (Critesion murinum) is the most common and inhabits disturbed areas (e.g. stock camps) in pastures, and sometimes in crops. Barley grass is divided into two subspecies murinum and subspecies leporinum: the latter tends to occur in drier areas.
\n• Squirrel tail grass (C. jubatum) has long soft awns (which may have a pink tinge) and is only found in damp salt pans in Central Otago.
\n• Salt barley grass (C. marinum) and Mediterranean barley grass (C. hystrix) mostly grow on salt-affected pastures, salty marshes, and coastal areas..
\n• C. secalinum is a perennial grass, unlike the other five, which are annuals, and is only found near Porangahau in coastal Hawkes Bay.
\n• Provides good-quality feed in autumn and during winter when plants are in the vegetative stage.
\n• Used for cover-cropping in Europe, in olive groves to prevent erosion in mountainous areas in Spain, and in vineyards in Turkey. An additional benefit is that barley grass tolerates drought well.',
-- impact
'• Barnyard grass is rarely a problem in pasture because its seeds cannot germinate in the shade of other plants and it germinates when pasture species are growing quickly.
\n• Barnyard grass competes with summer-active crops, producing a considerable bulk of vegetation in late spring.
\n• It is a major weed of rice, and is known to reduce yields in maize and other crops.',
-- control
'• Cultivation or mowing before plants set seed can give useful control in some situations
\n• Crop rotation can be a useful tool for limiting the build-up of weeds. Continuous cropping with the same crop builds up weeds that match the growth patterns of the crop. This should be avoided if at all possible by alternating maize, for example, with non-grass crops
\n• Weeds in maize are usually controlled with a mixture of pre-emergence herbicides The most common combination used in New Zealand is a mixture of a triazine, such as atrazine or terbuthylazine for broadleaf control, and a chloroacetamide like alachlor, metolachlor or acetochlor for the control of grass weeds.
\n• Pre-emergence herbicides must be activated either by mechanical incorporation or by rainfall before it can be taken up by emerging weed seedlings.
\n• As the crop grows it is important to monitor for weeds that have emerged despite the pre-emergent herbicide, so that post-emergent herbicides like nicosulfuron, mesotrione or topramezone can be applied early enough to be effective.',
-- further_info
'• Healy AJ, Edgar E 1980. Flora of New Zealand. Volume III. Adventive cyperaceous, petalous & spathaceous monocotyledons. First electronic edition, Landcare Research, June 2004. Transcr. AD Wilton and IML Andres. (accessed 4 October 2016).
\n• Weed management for maize. FAR Focus 11, Foundation for Arable Research, October 2013. (accessed 4 October 2016).
\n• Popay I, Champion P, James T 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.');

-- 12
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Acaena novae-zelandiae, A. anserinifolia', 'Bidibidi or piripiri',
-- key_char
'• Prostrate, perennial herb with slender, woody stems.
\n• Leaves composed of 9-15 pairs of leaflets (pinnate leaves).
\n• Leaflets oblong and deeply toothed.
\n• Flower heads spherical and comprising many segments, each with a long, hooked spike when fruiting.
\n• A. novae-zelandiae leaves are bright and shiny with pale-green undersides.
\n• A. anserinifolia leaves are dull brownish-green with silvery, hairy undersides.
\n• A. anserinifolia also has smaller flower heads.',
-- bio
'• Both species are native to New Zealand
\n• A. novae-zelandiae is also found in Australia and Papua New Guinea
\n• It has become a weed in California, Great Britain and Ireland.
\n• Found throughout New Zealand, although is less common on the West Coast of the South Island.
\n• Perennial herbs with a stoloniferous growth habit.
\n• New plants grow from seed.
\n• Seed dispersal is aided by the hooked spikes, which latch on to and are spread by animals.
\n• A. novae-zelandiae has been used for ground cover in gardens or as a lawn substitute but more commonly a related species A. inermis purpurea is now used in this role.
\n• It has been suggested that dried tips of young leaves of A. anserinifolia may be brewed as tea.',
-- impact
'• Invasive in poor or broken pastures, limiting grass growth and pasture utilisation.
\n• Impacts on forage crops.
\n• Unlikely to invade cultivated or cropped land.
\n• The hooked seeds latch onto sheep’s wool, interfering with shearing and down grading the value of the fleece.
\n• Likely to have a similar impact on other fleece bearing animals such as alpaca.',
-- control
'• Unaffected by lax grazing or set stocking
\n• Mob stocking (heavy on-and-off grazing) may reduce flowering and seed set
\n• Improved pastures may reduce the incidence of this weed.
\n• The phenoxy herbicide 2,4-D has a label claim to control or severely suppress this weed, however, farmers in some regions say it has little impact.
\n• Picloram based herbicides may offer greater suppression but will also severely damage clovers.
\n• Anecdotal reports indicate glyphosate has little impact.
\n• Effect of metsulfuron unknown.',
-- further_info
'• Holden P 2020. New Zealand Novachem Agrichemical Manual. Agrimedia Ltd, Christchurch, New Zealand. 924 p.
\n• Popay I, Champion P, James T 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.
\n• Poole A. 1966. Bidi-bidi (Acaena spp.). Te Ara: the Encyclopedia of New Zealand. Ministry for Culture and Heritage, Wellington, N.Z. (accessed 21 August 2020).
\n• Landcare Research Maanaki Whenua. Ngā Tipu Whakaoranga, Māori Plant Use database: Acaena anserinifolia. Piripiri. Hutiwai. Bidibid. (accessed 21 August 2020).');

-- 13
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Cardamine hirsuta', 'Bitter cress',
-- key_char
'• Small, rosette-based annual up to 25 cm tall.
\n• Leaves are deep green, lobed and sparsely hairy. Each leaf has two or three pairs of rounded leaflets with a larger terminal lobe.
\n• Upright flower stems carry few leaves and many tiny white flowers in small clusters.
\n• Flowers are 4-5 mm across with four petals, each twice as long as the four sepals, and four stamens with yellow anthers.
\n• Flowers are followed by small, slender, upright pods 15-25 mm long. Two valves split explosively and coil upwards, spreading the seeds up to a metre from the parent plant.
\n• Wavy bitter cress (Cardamine flexuosa) is similar but often slightly larger with a wavy erect stem and six stamens in the flower. It is scattered throughout New Zealand and found in wetter environments than bitter cress.
\n• The native New Zealand bitter cress (Cardamine debilis) is similar to bitter cress but has larger flowers, each with six stamens. It is found throughout New Zealand, in a range of forest or tussock habitats.
\n• Cuckoo cress (Cardamine pratensis) is a rhizomatous perennial herb up to 60 cm tall. It has larger pink flowers and is found in wet places and along river banks in Northland, Auckland, Waikato, Manawatu and Horowhenua in the North Island and in Westland and Southland in the South Island.',
-- bio
'• Originally from Europe and western Asia, bitter cress has now been introduced to North America, eastern Asia, Australia and New Zealand.
\n• First recorded in New Zealand in 1901.
\n• Flowers August to December. Plants can set seed within a few weeks of germinating, so several generations can occur in a year.
\n• One plant can produce up to 5000 seeds that can germinate immediately. However, if the seeds are in environments that do not favour germination they can survive for several years.
\n• Seeds are small and sticky when wet so can stick to footwear, enabling them be transported and dispersed.
\n• In a moist environment bitter cress can probably germinate, grow and set seed at any time of the year.
\n• Leaves have a hot, cress-like flavour and have been used as a garnish or flavouring in salads.
\n• Now found throughout the North Island and in eastern areas of the South Island, as well as on Stewart and Chatham Islands.
\n• Commonly found in damp gardens, along driveways, in cultivated or disturbed ground and can also be found growing in plant pots.',
-- impact
'• Bitter cress is probably not very competitive as a weed although if many individual plants germinate together they could limit the growth of later germinating species.
\n• Seeds generally do not germinate in the presence of competitive or shading vegetation such as pasture.
\n• Plants can act as hosts for common garden pests such as aphids.
\n• Wavy bitter cress is more abundant in Poverty Bay and has been noted as a weed of arable crops in that region.
\n• Bitter cress is rarely a pasture weed although it could interfere with establishment of a new pasture if present in high numbers
\n• Young stems with their soft, finely-divided leaves break easily but later become tougher and can sprawl for long distances.',
-- control
'• Hand weeding is very effective but must be repeated regularly, preferably before the plants set seed. Individual plants are easy to dislodge and uproot. Uprooted fruiting plants can continue shedding seed.
\n• Bitter cress is usually found in open places and the seeds probably don’t germinate under the cover of vegetation.
\n• Bitter cress also germinates from very close to the surface (less than 10 mm deep) and will not grow if the soil surface is dry. It germinates best in compacted, damp soils.
\n• Bitter cress (Cardamine hirsuta) is readily controlled by a wide range of herbicides including 2,4-D, glyphosate and many of those normally used in crop production.',
-- further_info
'• Popay I, Champion P, James T 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.');

-- 14
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Pteridium esculentum', 'Bracken',
-- key_char
'• Bracken is a fern, producing spores not seeds, which is native to New Zealand.
\n• It spreads by means of underground stems (rhizomes) that send up leaves at intervals.
\n• It is taller-growing than ring fern, usually up to 1.5 m tall.
\n• Rhizomes are stiff, 5-15 mm thick, and branch frequently.
\n• Stipes (leaf stalks) are erect, rigid, dark brown, glossy but hairy when young.
\n• The main axis of the leaf is stout, brown and hairy when young.
\n• Fronds (leaves) are dark green, up to 1 m long, unrolling as they grow.
\n• Spore-bearing organs (sporangia) are borne along the underside margins of the smallest leaf segments.
\n• Although bracken has been used as human food in New Zealand, parts of the plant are toxic and carcinogenic to humans and livestock.
\n• Plants are very ‘plastic’ in behaviour, being small and stunted in dry rocky places and sometimes reaching 4 m high on forest margins.
\n• Dry, dead fronds burn very readily.',
-- bio
'• Bracken, like ring fern, is a native to New Zealand. Pteridium esculentum is also found in Australia and the Society Islands but Pteridium aquilinum, a very close relative, is widespread throughout the world.
\n• Pteridium esculentum rapidly increased in area in New Zealand as early humans cleared and burned forests and it is now common throughout the country in open habitats.
\n• Bracken is a fern, reproducing by spores that germinate to produce a small prothallus This develops male and female sexual organs that in turn produce male and female gametes, resulting in the formation of a new fern plant.
\n• Bracken spores are very small and are released between late summer and autumn They can be carried for considerable distances on air currents.
\n• Bracken rhizomes were used by Maori as a starchy food.
\n• Dry bracken stalks have multiple uses as play things, from arrows to kite structures.',
-- impact
'• Tall-growing bracken can make stock access and mustering very difficult.
\n• Bracken, like ring fern, can form very dense cover, smothering useful pasture species.
\n• Bracken uses valuable soil nutrients for growth and these nutrients are locked up in the fronds until they eventually break down.
\n• Some strains of bracken appear to be more toxic than others, but all can be poisonous to livestock if large quantities are eaten.
\n• Bracken contains carcinogens that can cause cancerous lesions in livestock.
\n• Bracken competes strongly with young trees and is also a fire risk.',
-- control
'• Bracken is rhizomatous and difficult to kill.
\n• Bracken commonly grows in poorer grazing land, therefore, its control may not be economically feasible.
\n• Grazing is not an effective method of control, but heavy treading by cattle can be used to crush the new fern shoots as they are emerging.
\n• Repeated mowing or crushing can be used as control measures. However, where bracken grows on steep hillsides this may not be practical.
\n• Establishment of new competitive pasture species, suited to local conditions, can be used after initial clearance of fern, and may, if adequately limed and fertilised, help to prevent reestablishment.
\n• Trees can form a dense canopy and shade out bracken but the trees must be protected from bracken when young.
\n• Bracken is generally very difficult to kill with herbicides, though it is susceptible to glyphosate and high rates of metsulfuron, both of which are damaging to grasses.
\n• Two selective herbicides – asulam and primisulfuron will control bracken within pine forests. Asulam should be applied without surfactant when releasing young trees.
\n• Asulam (Asulox) is selective in pastures and should be applied when bracken fronds are fully expanded but before they are affected by frost (late summer to early autumn). Its effect on the bracken will not be obvious until the following spring.
\n• No biological control agents are available for either species.',
-- further_info
'• Massey University Weeds Database 2014. Bracken: Pteridium esculentum (accessed 19 May 2015).
\n• McGlone MS, Wilmshurst JM, Leach HM 2005. An ecological and historical review of bracken (Pteridium esculentum) in New Zealand, and its cultural significance. New Zealand Journal of Ecology 29: 165-184.
\n• Popay I, Champion P, James T 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.
\n• Young S 2013. New Zealand Novachem Agrichemical Manual. Agrimedia Ltd, Christchurch, New Zealand. 767 p.');

-- 15
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Panicum miliaceum', 'Broom corn millet',
-- key_char
'• Leaves are grass-like but broad, up to 2 cm wide, and resemble maize or sorghum but for the long hairs on the leaf sheath.
\n• Leaf blades hairy on upper and lower surfaces and along edges.
\n• Leaf sheaths are very hairy and the margins overlap.
\n• Ligules consist of a line of dense hairs.
\n• Flower spikelets individually borne on the end of branched panicles, which can be between 15 – 30 cm long.
\n• Seeds are egg-shaped and encased in a shiny seed coat approximately 3 x 2 mm in size.
\n• Seedlings grow rapidly into upright plants.
\n• Roots are shallow and weak, making plants easy to uproot.',
-- bio
'• Originated in the tropics and temperate regions and has been grown as a domestic crop for at least 2000 years.
\n• Broom corn millet is a widely grown crop for human consumption and birdseed in the northern hemisphere.
\n• In 1970, a wild biotype with black seeds emerged and quickly became weedy, producing more dry matter, reaching a greater height and producing twice as much seed.
\n• Germination starts at the beginning of the warm season and continues throughout the growing season.
\n• Seeds have no dormancy and can germinate rapidly once conditions are suitable.
\n• Because of its large seed size, seeds can emerge from deep within the soil. In one study seeds emerged from 120 mm in a range of soil types.
\n• Growth is rapid and is mainly determined by temperature as it uses a C4 photosynthetic pathway.
\n• Flowering normally begins 30 days after germination and seed production continues for a long period..
\n• Plants set seed rapidly if under stress and can set viable seed within 6 weeks of emergence.
\n• It is grown as a seed crop and used for human consumption. It can grow in dry climates.',
-- impact
'• Broom corn millet reduces crop yields by competition and interferes with harvest by clogging machinery. In one study, it was shown to reduce crop yield by 13 –22%, when present at a density of 10 plants/m2.
\n• Competes with maize and sweet corn for water and nutrients early in its life cycle. Later, when it has become tall enough, it competes for sunlight as it can reach over 2 m high in crops.',
-- control
'• Originated in the tropics and temperate regions and has been grown as a domestic crop for at least 2000 years.
\n• Broom corn millet is a widely grown crop for human consumption and birdseed in the northern hemisphere.
\n• In 1970, a wild biotype with black seeds emerged and quickly became weedy, producing more dry matter, reaching a greater height and producing twice as much seed.
\n• Germination starts at the beginning of the warm season and continues throughout the growing season.
\n• Seeds have no dormancy and can germinate rapidly once conditions are suitable.
\n• Because of its large seed size, seeds can emerge from deep within the soil. In one study seeds emerged from 120 mm in a range of soil types.
\n• Growth is rapid and is mainly determined by temperature as it uses a C4 photosynthetic pathway.
\n• Flowering normally begins 30 days after germination and seed production continues for a long period.
\n• Plants set seed rapidly if under stress and can set viable seed within 6 weeks of emergence.
\n• Broom corn millet reduces crop yields by competition and interferes with harvest by clogging machinery. In one study, it was shown to reduce crop yield by 13 –22%, when present at a density of 10 plants/m2.
\n• Competes with maize and sweet corn for water and nutrients early in its life cycle. Later, when it has become tall enough, it competes for sunlight as it can reach over 2 m high in crops.
\n• It is grown as a seed crop and used for human consumption. It can grow in dry climates.',
-- further_info
'• Wilson RG, Westra P. 1991. Wild Proso Millet (Panicum miliaceum) interference in corn (Zea mays). Weed Science 39: 217-220.
\n• James TK, Rahman A, Trivedi P. Broom corn millet (Panicum miliaceum): a new menace for maize and sweetcorn growers in New Zealand. Proceedings of the Seventeenth Australasian Weed Conference, Ed. Zydenbos SM (New Zealand Plant Protection Society), pp 32-35.');

-- 16
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Orobanche minor', 'Broomrape',
-- key_char
'• Parasitic plant lacking in green colouration
\n• 1-2 cm long, sparsely spaced, scale-like leaves are the same colour as the stem. They can be hairless or have glandular hairs.
\n• Fleshy-stemmed flower stalks, 10-40 cm tall and about 1 cm across, are the only visible part of plant.
\n• Flower stalks are light tan to brown and sometimes purple coloured.
\n• Unscented tubular flowers, 10-15 mm across, yellowish, with many bluish-mauve veins, appear on upper part of flower stalk between August and January.
\n• Orange-brown root tubers attach to roots of legumes, dandelions and some other plants including shrubs.
\n• Tarweed (Parentucellia viscosa) and red tarweed (Parentucellia latifolia) are similar parasitic weeds, but both have sticky green leaves.
\n• Tarweed has yellow flowers and the other red flowers. Tarweed is common on roadsides while red tarweed is rare and only found in pastures in a few parts of the North Island.',
-- bio
'• Native to western Europe and higher altitudes in Africa.
\n• Broomrape was first found in New Zealand in 1867, near Whangarei, and is now a common weed of crops and pastures and waste places throughout the country.
\n• Produces seeds that are about 1/3 of a mm long and readily spread by wind.
\n• The tiny seeds are stimulated to germinate by secretions from the roots of host plants.
\n• The emerging root of the broomrape seed attaches itself to a root of the host plant and derives all its nutrition from those plants; lacking chlorophyll, they cannot make food for themselves.
\n• The plants are perennial, sending up a new flowering shoot each spring and summer for a number of years or until the host plant dies.
\n• Plants occur on roadsides, disturbed ground, in open pastures and in crops on heavy soils.
\n• None that we know of.',
-- impact
'• Probably limited effects, although presumably host plants such as clovers are weakened by this parasitic plant
\n• Other species of broomrape (especially Orobanche ramosa and Orobanche aegyptiaca) found overseas are considered serious weeds in some crops but these are not found in New Zealand
\n• Seeds of these other species are considered serious contaminants of crop seeds in international trade.
\n• No direct effects.',
-- control
'• In New Zealand, control of this species is not usually necessary, although it has caused yield losses in New Zealand tobacco crops.
\n• Mowing will reduce seed set or remove unsightly flower heads on lawns and grass berms.
\n• For other broomrape species found overseas, no single, cheap method of control is effective, so integrated control methods must be used for these more serious species.
\n• Usually ignored by livestock.
\n• Diquat provides effective control in wasteland areas or prior to cultivation or crop establishment.
\n• The broomrape-fly Phytomyza orobanchia was widely used for Orobanche control in the Soviet Union and some East European countries in the 1960s and 1970s, but Orobanche is not important enough here to warrant its introduction.
\n• Trap crops and catch crops are used for control of Orobanche species overseas.
\n• These crops stimulate germination of Orobanche in the soil to deplete the seed reserves.
\n• Trap crops promote Orobanche seed germination but do not support parasitism.
\n• Catchcrops support parasitism but are destroyed prior to Orobanche flowering.',
-- further_info
'• CABI 2014. Orobanche minor. Invasive Species Compendium. (accessed 14 October 2014) https://www.cabidigitallibrary.org/doi/10.1079/cabicompendium.37746
\n• Habimana S, Nduwumuremyi A, Chinama JD 2014. Management of Orobanche in field crops – A review. Journal of Soil Science and Plant Nutrition 14: 43-62. (accessed 13 October 2014) https://www.scielo.cl/scielo.php?pid=S0718-95162014000100004&script=sci_arttext
\n• James RW, Frater KC 1977. The control of broomrape (Orobanche minor) in flue-cured tobacco. New Zealand Tobacco Growers Journal October: 10-13.
\n• Popay I, Champion P, James TK 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.');

-- 17
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Buddleja davidii', 'Buddleia',
-- key_char
'• Fast growing, multi-stemmed, deciduous woody shrub up to 3 m tall.
\n• Mauve to purple flowers (occasionally white) in large, showy, spike-like panicles about 30 cm long.
\n• Flowers attractive to butterflies.
\n• Individual flowers about 5 mm across, mauve or purple, with orange colour inside the petal tube.
\n• Leaves lance-shaped, up to 20 cm long and 8 cm wide, green and hairless on top, whitish and hairy underneath.
\n• Four other naturalised species are found in New Zealand, the commonest being Buddleja globosa, which has globe-shaped inflorescences and is found in forest remnants near habitations.',
-- bio
'• Native to China.
\n• Commonly grown in gardens for its decorative and butterfly-attracting flowers.
\n• First found growing wild (that is, naturalised), before 1940.
\n• Now a common shrub in hedgerows, along roadsides, in forests, on river banks and in waste places throughout the country; less common in southern South Island.
\n• Subject to Pest Plant Management Strategies in several regions.
\n• Small, light seeds dispersed by wind and water.
\n• Plant can reach maturity and flower within one year.
\n• Grows quickly and aggressively, and can reach 4 m high after two years; infestations rapidly form dense thickets that out-compete other vegetation.
\n• Plants are relatively short-lived with infestation densities peaking within 10 years.
\n• By about 15 years plant densities are reduced, and native trees, if present, eventually dominate again.
\n• Tolerates frosts and grows well under a wide range of environmental conditions. 
\n• The flowers are attractive to butterflies and gardeners.',
-- impact
'• Most important weed in central North Island plantation forestry.
\n• Reduces growth of plantation species.
\n• Costs the forestry industry about $2.9 million a year in control and lost production.
\n• Readily colonises disturbed sites such as slips and stream beds, outgrowing native colonising species.
\n• Changes plant communities, hinders access and shades rivers.
\n• Difficult to control where access is difficult and because plants grow rapidly.
\n• In riverbeds, buddleia can change water flow, divert streams, cause silt to build up, and can cause flooding problems.
\n• Interferes with the regeneration of native species.',
-- control
'• Leaves are palatable to cattle and goats but not, apparently, to deer.
\n• Small plants can be pulled or dug out and then mulched.
\n• Plants that are cut will regrow.
\n• Shoot or root fragments left on the ground can root and regrow.
\n• Painting cut stumps or stems with herbicides like picloram (Tordon), triclopyr or metsulfuron-methyl kills the whole plant.
\n• Plants with larger stems can be killed by frilling (making deep cuts into the sapwood around the stem) or drilling holes into the wood and then applying appropriate herbicides like glyphosate (250 ml/L) or undiluted Tordon Brushkiller.
\n• Basal stem treatments with X-tree Basal or triclopyr/diesel mix.
\n• Weed wiping foliage with glyphosate at 333 ml/L (in February-April) is effective on smaller shrubs.
\n• Spraygun application in February-April with glyphosate (10 ml/L), metsulfuron-methyl 600 g/kg (5 g/10 L), or Tordon Brushkiller at 90 ml/15 L (knapsack) or 250 ml/100 L gives effective control of larger bushes and infestations.
\n• Buddleia leaf weevil (Cleopus japonicus) was released in New Zealand in 2006.
\n• Adults and larvae feed on the leaves.
\n• Leaves with extensive damage become silvery-brown, curl and drop to the ground.
\n• Oversowing cover grasses such as Yorkshire fog (Holcus lanatus) can effectively prevent or limit establishment of buddleia seedlings.',
-- further_info
'• Popay I, Champion P, James TK 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.
\n• Weedbusters, 2016, Buddleja davidii Factsheet (accessed 14 October 2016).');

-- 18
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Arctium minus, A. lappa', 'Burdock',
-- key_char
'• Tall, many-branched, upright herb to 1.5 m high.
\n• Large, hairy, triangular leaves (40 x 30 cm).
\n• Spiky, pink, thistle-like flower head about 3 cm long.
\n• Flower heads in clusters at the ends of branches.
\n• A. minus has hollow-stalked leaves while the lower leaves of A. lappa are solid.
\n• A. lappa has larger flower heads with longer stalks.',
-- bio
'• Both species come from Europe/Asia and were introduced to New Zealand in the late 19th century.
\n• A. minus is occasionally found in waste places, roadsides, bush margins and sheep yards throughout both North and South Islands, except in Westland. Most abundant in Manawatu.
\n• A. lappa is found in only a few locations in the lower South Island. Was present near Morrinsville in Waikato but now possibly eliminated from the North Island.
\n• Burdock is a biennial (living through two growing seasons) herb with new plants growing from seed.
\n• Burdock has a large seed about 5 mm long and although it has a small pappus, it is too large for wind dispersal and relies on the hooked spikes on the seed head for its spread.
\n• In the first year, plants form a rosette of large, hairy, triangular leaves, dying off to the root system during winter. In the second year, a tall branched flowering plant develops, that dies completely after fruiting.
\n• Young flowering stems and young shoots of burdock can be eaten.
\n• The root is used in many herbal remedies where it is reputed to be one of the best cleansers, especially for skin ailments.',
-- impact
'• Burdock is only a nuisance in poor, runout pastures or in scrubby, broken hill country
\n• When present in pasture, burdock will restrict grazing resulting in reduced pasture utilisation.
\n• As a biennial plant burdock is unlikely to be a persistent weed in annual forage crops. It is also unlikely to persist in perennial crops (e.g. lucerne) which are mown at least once a year.
\n• The burs are a major problem to sheep farming where they attach to the wool, causing problems with shearing and possibly rendering the fleece worthless.',
-- control
'• Young burdock plants may not survive intensive mob stocking but once established will not be grazed.
\n• May be controlled by mowing although generally only found in low numbers and hand grubbing will be effective.
\n• Burdock is reputed to indicate low pH and a requirement for lime.
\n• Burdock seedlings are readily controlled by the phenoxy herbicides MCPA and 2,4-D.
\n• Larger plants controlled with the addition of picloram.
\n• Burdock is listed in some Regional Pest Management Strategies and it is an offence to knowingly move the plant or its seed into these regions. Look at the on-line RPMS for your regional council for more information.',
-- further_info
'• Holden, P 2020. New Zealand Novachem Agrichemical Manual. Agrimedia Ltd, Christchurch, New Zealand. 924 p.
\n• Popay I, Champion P and James T 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Lincoln, New Zealand. 416 p.
\n• Dawson M, Navie S, James T, Heenan P, Champion, P 2007–2019. Weeds Key – interactive key to the weed species of New Zealand (Accessed 20 July 2020).
\n• Auckland Council. Burdock. Arctium minus (accessed 20 July 2020).
\n• Douglas MH, Burgmans JL, Burton LC, Smallfield BM 1992. The production of Burdock (Arctium lappa L .) root in New Zealand – a preliminary study of a new vegetable. Proceedings Agronomy Society of New Zealand, 22: 67-70 (accessed July 20 2020).');

-- 19
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Stellaria media', 'Chickweed',
-- key_char
'• A sprawling annual plant with long, trailing, easily-broken stems, and many soft, pale green leaves.
\n• Flowers are in loose clusters each flower about 1 cm across with five, fine, white and very deeply divided petals.
\n• Leaves are light green, hairless (but with short hairs on the margins towards the stalk), oval shaped with a pointed tip and in opposite pairs on hairy stalks.
\n• Fine hairs run along one side of the stems/branches that rotate position by 90° at each node.
\n• To distinguish chickweed from other plants, the stem may be pulled so that it breaks around the outside. The centre of the stem will stretch if it is chickweed.',
-- bio
'• Native to Europe.
\n• Spread throughout the world by humans as the plant has been widely used as a vegetable and as a herbal remedy.
\n• Chickweed is very common throughout New Zealand, growing quickly in arable crops, pastures, gardens, lawns and waste places.
\n• Bare ground and pastures damaged by winter pugging are very vulnerable to chickweed invasion.
\n• Chickweed can grow in denser shade and at lower temperatures than many other weeds.
\n• Chickweed can grow over the winter months but does not survive dry conditions and dies back in most summers.
\n• Its prevalence increases as soils become more fertile.
\n• Chickweed usually germinates in autumn or winter and grows through winter and early spring.
\n• Chickweed is an annual, producing flowers and seed very quickly.
\n• Small seeds are easily dispersed in mud or dirt. Up to 2500 can be produced per plant, which means millions of seeds are often buried in the soil.
\n• Some seeds germinate within a few months of dispersal provided conditions are favourable, but others can last in the soil for years. It takes 3 years for the seed bank to be reduced by 50% and about 18 years to deplete the seedbank by 99%.
\n• When conditions are right i.e. damp, disturbed soil or bare patches, the stems of chickweed can root at the nodes.
\n• Both plants and seeds are readily eaten by birds, make useful fodder for lambs, and are said to increase the output of hens’ eggs.
\n• Leaves and young shoots are used in green salads and boiled as a potherb in several countries from India to North America, although the flavour becomes bitter with age.',
-- impact
'• Chickweed can be persistent in high producing pastures, especially in cool or shady conditions.
\n• This weed can shade and smother young crop seedlings because its mat-like growth makes it a strong competitor.',
-- control
'• Although livestock do not readily eat chickweed, it may be controlled by trampling during grazing.
\n• Pugging in winter should be avoided where possible.
\n• Improved drainage may help reduce chickweed.
\n• Harrowing breaks the tender stems and reduces its competitive growth.
\n• Chickweed is fairly tolerant to foliar applications of MCPB, 2,4-DB, 2,4-D and MCPA
\n• Dicamba controls chickweed but also damages clovers.
\n• Several herbicides used in field/horticultural crops control chickweed effectively.',
-- further_info
'• Popay I, Champion P, James T 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.
\n• Young S 2013. New Zealand Novachem agrichemical manual. Agrimedia Ltd, Christchurch, New Zealand. 767 p.');

-- 20
INSERT INTO `guide_info` (`item_type`, `name`, `common_name`, `key_char`, `bio`, `impact`, `control`, `further_info`)
VALUES
('weed', 'Rorippa sylvestris', 'Creeping yellow cress',
-- key_char
'• Wide spreading, straggling, rhizomatous perennial herb usually 20- 50 cm tall.
\n• Yellow flowers, with four petals, 4-6 mm across, appear in loose clusters at the top of the flower stem from December to February.
\n• Seed pods curved, 10-15 mm long, on stalks of similar length.
\n• Leaves hairless, deeply divided into 4 to 10 lobes. Smaller leaves with fewer lobes on flower stalk.
\n• Creeping rhizomes can result in dense mats of foliage that smother infested land or crops.
\n• Marsh yellow cress or poniu (Rorippa palustris) is native to New Zealand, although there are also races of the same species that have been introduced from elsewhere. Flowers are paler, leaves less divided, and seed pods shorter and wider than those of creeping yellow cress. Marsh yellow cress is not as common but it is also found in wet places throughout the country.',
-- bio
'• Native to temperate Europe and southwest Asia.
\n• First recorded in New Zealand in 1952 but most likely was here much earlier and perhaps overlooked or confused with other species.
\n• Now common in places throughout the North and South Islands.
\n• A common garden weed, also found in market gardens, under tree crops and on cultivated land (especially headlands), as well as in damp pasture and river beds.
\n• Creeping yellow cress can be a very persistent weed and is hard to eradicate because of its rhizomes.
\n• Spread is by means of rhizomes and rhizome fragments, as well as by seed.
\n• Some local populations do not produce seed because plants are self-incompatible.
\n• Plant may produce allelochemicals that inhibit the germination of other plant species.
\n• Can withstand prolonged submergence under water.
\n• Hybridises with other species of Rorippa.
\n• Rhizome fragments can be moved in plants bought from nurseries or elsewhere. 
\n• None that we know of.',
-- impact
'• Can form dense, tangled masses of stems and intertwining rhizomes floating in water or creeping over mud.
\n• Stems and rhizomes may be several metres long, and can root at several points.
\n• Especially a problem in nurseries, from which it can easily be spread with ornamental plants sold in containers.
\n• The creeping rhizomes can create a thick mat of weed which completely smothers pasture.
\n• A pioneer species, preferring to grow on bare soil or mud..
\n• A common weed of waterways, wetlands, swamps, lakes, ponds and other wetter habitats in temperate and sub-tropical regions.',
-- control
'• Pastures should be kept dense in autumn to prevent creeping yellow cress from establishing. This can be done by selection of appropriate grass cultivars or by grazing management.
\n• Creeping yellow cress is not affected by many common pre-emergence herbicides.
\n• Flumetsulam controls creeping yellow cress without adversely affecting clovers and grasses. It should be applied before flowering and repeat applications may be necessary in subsequent years.
\n• In other countries, triclopyr + dicamba have given effective control but this combination will kill many other plants except grasses.
\n• MCPA or 2,4-D will give at least temporary suppression.
\n• Glyphosate kills the top growth but regrowth takes place afterwards.
\n• It is more important to prevent nurseries becoming infected with this weed as getting rid of it after it has invaded can be very difficult.
\n• Hand pulling of plants is likely to leave behind root or rhizome fragments that can later regrow.
\n• Cultivation probably spreads the weed rather than controlling it.',
-- further_info
'• Popay I, Champion P, James TK 2010. An illustrated guide to common weeds of New Zealand. New Zealand Plant Protection Society, Christchurch, New Zealand. 416 p.');

-- create image store table
CREATE TABLE `image`(
	`image_id` INT AUTO_INCREMENT,
    `guide_id` INT,
    `image_path` VARCHAR(255),
    `is_primary` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`image_id`),
    FOREIGN KEY (`guide_id`) REFERENCES `guide_info`(`guide_id`)
);

-- INSERT INTO `image` (`image_id`, `guide_id`, `image_path`, `is_primary`)
-- VALUES



