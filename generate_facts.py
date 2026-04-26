import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# Read population data
with open(os.path.join(BASE, 'population-data.json'), 'r', encoding='utf-8') as f:
    countries = json.load(f)

# Facts collected from websites + knowledge, adapted for primary school age
facts_map = {
    "India": [
        "India has a floating post office on a boat in a lake in Srinagar.",
        "The game Snakes and Ladders was invented in India long ago to teach kids about good and bad.",
        "India produces the most mangoes in the world, over 20 million tonnes every year!",
        "India is the birthplace of chess.",
        "The number system we use today (0,1,2,3...) was invented by Indian mathematicians."
    ],
    "China": [
        "China has the longest bridge in the world, the Danyang-Kunshan Grand Bridge, which is 164 kilometers long!",
        "In China, every year has an animal name, like the Year of the Tiger or Year of the Dragon.",
        "China built a giant solar power plant shaped like a panda bear that you can see from space!",
        "All of China uses one time zone, even though the country is big enough to have 5 time zones.",
        "Table tennis (ping pong) is the most popular sport in China."
    ],
    "United States": [
        "The US flag with 50 stars was designed by a high school student for a class project.",
        "The United States and Canada share the longest border in the world that has no soldiers guarding it.",
        "One third of all the airports in the world are located in the US.",
        "The Internet was first thought up in the United States."
    ],
    "Indonesia": [
        "Indonesia is made up of over 17,000 islands, making it the largest island nation in the world!",
        "Indonesia is home to the Komodo dragon, the biggest lizard on Earth.",
        "Indonesia has the largest Muslim population in the world."
    ],
    "Pakistan": [
        "A small city called Sialkot in Pakistan makes 40% of all the soccer balls used in the world!",
        "Pakistan has the second largest Muslim population in the world."
    ],
    "Nigeria": [
        "Nigeria is home to over 520 different languages spoken by its people!",
        "Nigeria has around 370 different tribes that are officially recognized."
    ],
    "Brazil": [
        "The Amazon Rainforest in Brazil provides about 20% of the world's oxygen.",
        "Brazil is famous for its Carnival celebration with colorful costumes and dancing in the streets.",
        "Brazil is the world's largest coffee producer, making about 35% of all coffee.",
        "Brazil has over 4000 airports!"
    ],
    "Bangladesh": [
        "Bangladesh is the most crowded large country in the world, with about 3,000 people living in every square mile.",
        "Bangladesh is the only country in the world whose name ends with the letter H."
    ],
    "Russia": [
        "Russia has 11 time zones, so the time difference between the east and west is about 10 hours!",
        "Russian scientists once grew a plant from a seed that was more than 30,000 years old.",
        "Russia has over 13,000 villages that nobody lives in anymore."
    ],
    "Ethiopia": [
        "Ethiopia uses a calendar that is 7 to 8 years behind the calendar most of the world uses.",
        "Ethiopia celebrates its New Year in September, not January!",
        "In 1974, scientists found a 3.2 million-year-old human skeleton in Ethiopia."
    ],
    "Mexico": [
        "Mexico is home to the largest pyramid in the world by volume, the Great Pyramid of Cholula. Its base is 4 times bigger than Egypt's Great Pyramid!",
        "A Mexican engineer invented the first color television system.",
        "Millions of monarch butterflies fly thousands of miles to and from Mexico every year."
    ],
    "Japan": [
        "Japan has more than 6,800 islands.",
        "Japan's bullet trains can travel up to 320 kilometers per hour!",
        "Japanese people live longer than almost anyone else in the world.",
        "In Japan, the green light on traffic signals looks blue because in Japanese culture blue and green are seen as shades of the same color."
    ],
    "Egypt": [
        "Bread was invented in Egypt around 8,000 years ago!",
        "Egypt is the most popular tourist destination in Africa, attracting around 10 million visitors per year."
    ],
    "Philippines": [
        "The Philippines is made up of over 7,600 islands!",
        "About a quarter of all overseas nurses in the world come from the Philippines."
    ],
    "DR Congo": [
        "The Democratic Republic of the Congo loves mayonnaise so much that people put it on almost everything!",
        "Belgium ruled this country from 1908 to 1960."
    ],
    "Vietnam": [
        "Vietnam is the world's largest exporter of cashew nuts and black pepper.",
        "The world's largest cave is located in Vietnam."
    ],
    "Iran": [
        "Iran has had 27 different capital cities in its history, more than any other country!",
        "McDonald's is not allowed to operate in Iran."
    ],
    "Turkey": [
        "Turkey has a dessert called tavuk gogsu that is made with shredded chicken breast, milk, sugar, and cinnamon!",
        "Istanbul in Turkey is the only city in the world that sits on two continents, Europe and Asia."
    ],
    "Germany": [
        "In Germany, everyone, even people from other countries, can go to college for free!",
        "Germany shares borders with 9 different countries."
    ],
    "Tanzania": [
        "Mount Kilimanjaro in Tanzania is the highest mountain in Africa, standing at 5,895 meters.",
        "Freddie Mercury, the famous singer from the band Queen, was born in Zanzibar, which is now part of Tanzania."
    ],
    "Thailand": [
        "Thailand is the only country in Southeast Asia that was never taken over by European countries.",
        "Thailand is the world's biggest exporter of rice.",
        "Every year Thailand holds a Monkey Buffet Festival where people give 4.5 tons of fruit and candy to 3,000 monkeys!"
    ],
    "United Kingdom": [
        "People in the UK drink 165 million cups of tea every day!",
        "The Industrial Revolution started in Britain.",
        "The longest town name in Europe is in Wales: Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch."
    ],
    "France": [
        "France is the most visited country in the world, with 89 million tourists every year.",
        "About 8 million people see the Mona Lisa painting at the Louvre museum in Paris every year.",
        "If you count overseas territories, France covers the most time zones of any country, 12 in total!"
    ],
    "South Africa": [
        "South Africa is called the 'Rainbow Nation' because it has 11 official languages!",
        "There is a street in Soweto called Vilakazi Street that was home to two Nobel Peace Prize winners: Nelson Mandela and Desmond Tutu."
    ],
    "Italy": [
        "Italians have only been eating tomatoes since the 1500s, when they were brought from Peru.",
        "Naples, Italy is the birthplace of pizza!",
        "There is a fountain in Italy that flows red wine 24 hours a day for people walking a pilgrimage."
    ],
    "Kenya": [
        "The Kalenjin tribe in Kenya produces the world's best long-distance runners.",
        "Kenya is home to the Big Five animals: lions, elephants, buffaloes, leopards, and rhinos."
    ],
    "Myanmar": [
        "Myanmar is one of only three countries in the world that does not use the metric system."
    ],
    "Colombia": [
        "Colombia produces some of the world's finest emeralds, green gemstones.",
        "Colombia has a river called Cano Cristales that looks like a 'liquid rainbow' with many vivid colors."
    ],
    "Sudan": [
        "In Arabic, the name Sudan means 'the land of the blacks'.",
        "Sudan actually has 223 pyramids, which is double the number of pyramids in Egypt!"
    ],
    "Uganda": [
        "Uganda is home to 11% of all the birds in the world!",
        "The endangered mountain gorilla lives in Uganda's Ruwenzori Mountains."
    ],
    "South Korea": [
        "In South Korea, people say 'kimchi' instead of 'cheese' when taking photos!",
        "Kimchi and rice are the two most important foods in South Korea, and this has been true for 3,000 years."
    ],
    "Algeria": [
        "Algeria is the largest country in Africa by land area.",
        "About 80% of Algeria is covered by the Sahara Desert."
    ],
    "Iraq": [
        "Iraq is often called the 'Cradle of Civilization' because some of the world's first cities were built there over 5,000 years ago.",
        "The capital city of Iraq is Baghdad."
    ],
    "Spain": [
        "Spain's national anthem has no words, so nobody sings along!",
        "The Sagrada Familia church in Barcelona has been under construction since 1882, longer than the pyramids took to build."
    ],
    "Argentina": [
        "Argentina is home to the world's widest street, Avenida 9 de Julio in Buenos Aires, which spans 140 meters!",
        "The tango dance was invented in the working-class neighborhoods of Buenos Aires, Argentina."
    ],
    "Afghanistan": [
        "Afghanistan's flag has a building on it.",
        "The capital city of Afghanistan is Kabul."
    ],
    "Canada": [
        "Canada has more lakes than every other country in the world put together!",
        "Canada's coastline stretches over 150,000 miles.",
        "Canada is the second-largest country in the world by area.",
        "The maple leaf has been a symbol of Canada since 1806."
    ],
    "Angola": [
        "More people speak Portuguese in Angola than in Portugal itself!",
        "Angola is one of the largest oil producers in Africa."
    ],
    "Ukraine": [
        "Ukraine is the largest country that is entirely within Europe.",
        "The world's worst nuclear accident happened at Chernobyl in Ukraine in 1986."
    ],
    "Morocco": [
        "Morocco is home to the world's oldest continuously operating university, founded in 859 AD.",
        "The capital city of Morocco is Rabat."
    ],
    "Poland": [
        "The flag of Poland is the reverse of Indonesia's flag: Poland has white on top and red on the bottom.",
        "The capital city of Poland is Warsaw."
    ],
    "Uzbekistan": [
        "Uzbekistan is one of only two countries in the world that are completely surrounded by other landlocked countries.",
        "The capital city of Uzbekistan is Tashkent."
    ],
    "Mozambique": [
        "Mozambique's flag is the only national flag that has a modern weapon on it, an AK-47 rifle.",
        "The capital city of Mozambique is Maputo."
    ],
    "Malaysia": [
        "The pomelo, the largest citrus fruit on the planet, comes from Malaysia.",
        "The Petronas Towers in Kuala Lumpur were once the tallest buildings in the world and are still the tallest twin towers."
    ],
    "Ghana": [
        "Ghana was the first country in sub-Saharan Africa to become independent from Britain.",
        "The capital city of Ghana is Accra."
    ],
    "Saudi Arabia": [
        "Saudi Arabia is the only country in the world that does not have any rivers!",
        "Saudi Arabia is home to the cities of Mecca and Medina, the two holiest cities in Islam."
    ],
    "Peru": [
        "Peru is home to Machu Picchu, an ancient Inca city high in the Andes mountains.",
        "Peru has more than 3,700 species of butterflies, which is 20% of all known butterfly species in the world.",
        "Peru grows more than 2,800 different types of potatoes, more than any other country."
    ],
    "Madagascar": [
        "Madagascar is home to animals that are found nowhere else on Earth, like lemurs.",
        "About 90% of all the plants and animals in Madagascar exist only on this island."
    ],
    "Ivory Coast": [
        "Ivory Coast is the world's largest producer of cocoa beans, which are used to make chocolate.",
        "The capital city of Ivory Coast is Yamoussoukro, but the biggest city is Abidjan."
    ],
    "Nepal": [
        "Nepal is home to Mount Everest, the highest mountain in the world at 8,848 meters.",
        "Nepal is the only country that does not have a rectangular flag. Its flag is shaped like two triangles."
    ],
    "Cameroon": [
        "Cameroon is often called 'Africa in miniature' because it has almost every type of landscape found on the continent.",
        "The capital city of Cameroon is Yaounde."
    ],
    "Venezuela": [
        "Venezuela is home to Angel Falls, the world's highest waterfall, which plunges 979 meters!",
        "Venezuela is named after the Italian word for 'Little Venice' because of houses built on stilts over water."
    ],
    "Niger": [
        "Niger is named after the Niger River, and the name comes from a local word meaning 'river of rivers'.",
        "The capital city of Niger is Niamey."
    ],
    "Australia": [
        "Australia is home to animals that lay eggs but also feed their babies milk, called monotremes. The platypus and echidna live there!",
        "The Great Barrier Reef off Australia's coast is the world's largest coral reef system.",
        "Australia has more kangaroos than people!",
        "There are no snakes in New Zealand, but Australia is home to many venomous snakes."
    ],
    "North Korea": [
        "North Korea claims to have a 100% literacy rate, meaning everyone there can read and write.",
        "In North Korea, there are only 15 approved hairstyles people can choose from."
    ],
    "Mali": [
        "Mali was once home to one of the richest empires in history, the Mali Empire, ruled by the famous king Mansa Musa.",
        "The capital city of Mali is Bamako."
    ],
    "Syria": [
        "The capital city of Syria is Damascus, which is one of the oldest continuously inhabited cities in the world.",
        "Syria is home to the ancient city of Palmyra."
    ],
    "Burkina Faso": [
        "Burkina Faso means 'Land of Incorruptible People' in the local languages.",
        "The capital city of Burkina Faso is Ouagadougou."
    ],
    "Sri Lanka": [
        "Sri Lanka was connected to India by a thin land bridge until 1480, making it one of the world's youngest islands.",
        "Sri Lanka has two official capitals: Colombo and Sri Jayawardenepura Kotte."
    ],
    "Malawi": [
        "Malawi is nicknamed 'The Warm Heart of Africa' because of the kindness of its people.",
        "The capital city of Malawi is Lilongwe."
    ],
    "Zambia": [
        "Zambia is home to Victoria Falls, one of the largest waterfalls in the world, which local people call 'The Smoke That Thunders'.",
        "The capital city of Zambia is Lusaka."
    ],
    "Kazakhstan": [
        "Kazakhstan is the largest landlocked country in the world.",
        "The capital city of Kazakhstan is Astana."
    ],
    "Chile": [
        "Chile is home to the driest desert on Earth, the Atacama Desert.",
        "Easter Island, famous for its giant stone heads called moai, belongs to Chile."
    ],
    "Romania": [
        "Romania is home to Transylvania, the region famous for the Dracula legend.",
        "The capital city of Romania is Bucharest."
    ],
    "Guatemala": [
        "The ancient Mayans built amazing pyramids and cities in Guatemala.",
        "Spanish is the official language of Guatemala, but 23 other languages are also spoken."
    ],
    "Chad": [
        "Chad is named after Lake Chad, which was once one of the largest lakes in Africa.",
        "The capital city of Chad is N'Djamena."
    ],
    "Somalia": [
        "Somalia has the longest coastline of any country in mainland Africa.",
        "The capital city of Somalia is Mogadishu."
    ],
    "Ecuador": [
        "Ecuador is named after the equator, which runs right through the country!",
        "The Galapagos Islands, which inspired Charles Darwin's theory of evolution, belong to Ecuador."
    ],
    "Netherlands": [
        "The Netherlands has the tallest people in the world on average!",
        "There are more bicycles than people in the Netherlands."
    ],
    "Senegal": [
        "Senegal is famous for its music, especially a type called mbalax.",
        "The capital city of Senegal is Dakar."
    ],
    "Cambodia": [
        "Cambodia has never had a McDonald's because the local food is so popular!",
        "The ancient temple of Angkor Wat in Cambodia is the largest religious monument in the world."
    ],
    "Zimbabwe": [
        "Zimbabwe has the highest literacy rate in Africa, meaning more people there can read and write than in any other African country.",
        "The capital city of Zimbabwe is Harare."
    ],
    "Guinea": [
        "Guinea is home to Mount Nimba, which has unique plants and animals found nowhere else.",
        "The capital city of Guinea is Conakry."
    ],
    "Rwanda": [
        "Rwanda has more women in its parliament than almost any other country in the world.",
        "Rwanda is known as the 'Land of a Thousand Hills' because of its many hills and mountains."
    ],
    "Benin": [
        "Benin was the birthplace of the vodun religion, which inspired the idea of 'voodoo'.",
        "The capital city of Benin is Porto-Novo."
    ],
    "Burundi": [
        "Burundi is one of the smallest countries in Africa but one of the most densely populated.",
        "The capital city of Burundi is Gitega."
    ],
    "Tunisia": [
        "Tunisia was home to the ancient city of Carthage, which was once one of the most powerful cities in the world.",
        "The capital city of Tunisia is Tunis."
    ],
    "Bolivia": [
        "Bolivia has the highest capital city in the world, La Paz, which sits at 3,650 meters above sea level.",
        "Bolivia and its neighbor Peru share Lake Titicaca, the highest navigable lake in the world."
    ],
    "Belgium": [
        "Belgium is famous for inventing French fries, called 'frites' there.",
        "The capital city of Belgium is Brussels, which is also the capital of the European Union."
    ],
    "Haiti": [
        "Haiti was the first country in the world led by people of African descent to become independent.",
        "The capital city of Haiti is Port-au-Prince."
    ],
    "Jordan": [
        "Jordan is home to the ancient city of Petra, which was carved into pink sandstone cliffs.",
        "The capital city of Jordan is Amman."
    ],
    "Dominican Republic": [
        "The Dominican Republic is called the 'Breadbasket of the Caribbean' because it grows so much food.",
        "The capital city of the Dominican Republic is Santo Domingo."
    ],
    "Cuba": [
        "Cuba is famous for producing some of the world's finest cigars.",
        "The capital city of Cuba is Havana."
    ],
    "South Sudan": [
        "The capital city of South Sudan is Juba.",
        "In South Sudan, people speak 2 main official languages, English and Arabic, but there are over 60 other local languages!"
    ],
    "Sweden": [
        "Sweden has 267,570 islands, more than any other single country in the world!",
        "The capital city of Sweden is Stockholm."
    ],
    "Czech Republic": [
        "The Czech Republic drinks more beer per person than any other country in the world.",
        "The capital city of the Czech Republic is Prague."
    ],
    "Honduras": [
        "Honduras is home to the ancient Mayan ruins of Copan.",
        "The capital city of Honduras is Tegucigalpa."
    ],
    "Greece": [
        "Greece is known as the birthplace of democracy, where people first voted to make decisions together.",
        "The ancient Greeks invented the Olympic Games over 2,700 years ago."
    ],
    "Azerbaijan": [
        "Azerbaijan is called the 'Land of Fire' because of natural gas fires that have been burning on its hills for thousands of years.",
        "The capital city of Azerbaijan is Baku."
    ],
    "Portugal": [
        "Portugal has the most sunshine hours in Europe, with some areas getting almost 300 sunny days a year.",
        "There are more Portuguese speakers outside Portugal than in it, especially in Brazil."
    ],
    "Hungary": [
        "Hungary is home to the largest thermal water cave system in the world.",
        "The capital city of Hungary is Budapest."
    ],
    "Tajikistan": [
        "Tajikistan is home to the Pamir Mountains, nicknamed the 'Roof of the World'.",
        "The capital city of Tajikistan is Dushanbe."
    ],
    "United Arab Emirates": [
        "The Burj Khalifa in Dubai, UAE, is the tallest building in the world at 828 meters.",
        "The capital city of the UAE is Abu Dhabi."
    ],
    "Belarus": [
        "Belarus is one of the most forested countries in Europe.",
        "The capital city of Belarus is Minsk."
    ],
    "Israel": [
        "Israel is home to the Dead Sea, which is so salty that people can float on the water without swimming.",
        "The capital city of Israel is Jerusalem."
    ],
    "Austria": [
        "Austria is famous for its classical music composers like Mozart and Beethoven.",
        "The capital city of Austria is Vienna."
    ],
    "Switzerland": [
        "Switzerland has the longest tunnel in the world, the Gotthard Base Tunnel, at 57.1 km.",
        "Switzerland eats the most chocolate per person in the world, about 10 kilos per person per year."
    ],
    "Togo": [
        "Togo is one of the world's largest producers of phosphate, which is used to make fertilizer.",
        "The capital city of Togo is Lome."
    ],
    "Sierra Leone": [
        "The capital city of Sierra Leone is Freetown.",
        "In Sierra Leone, English is the official language, but people use about 25 different languages every day."
    ],
    "Laos": [
        "Laos is the only landlocked country in Southeast Asia.",
        "The capital city of Laos is Vientiane."
    ],
    "Paraguay": [
        "Paraguay has a large hydroelectric dam shared with Brazil that produces almost all of Paraguay's electricity.",
        "The capital city of Paraguay is Asuncion."
    ],
    "Libya": [
        "Libya has the highest percentage of desert in the world, with 99% of its land being desert.",
        "The capital city of Libya is Tripoli."
    ],
    "Bulgaria": [
        "In Bulgaria, nodding your head means 'no' and shaking your head means 'yes', which is the opposite of most countries!",
        "The capital city of Bulgaria is Sofia."
    ],
    "Serbia": [
        "Serbia is home to the oldest known human settlement in Europe, Lepenski Vir, which is over 8,000 years old.",
        "The capital city of Serbia is Belgrade."
    ],
    "El Salvador": [
        "El Salvador is the smallest country in Central America.",
        "The capital city of El Salvador is San Salvador."
    ],
    "Nicaragua": [
        "Nicaragua is home to Lake Nicaragua, the only freshwater lake in the world that has ocean-like sharks in it.",
        "The capital city of Nicaragua is Managua."
    ],
    "Kyrgyzstan": [
        "Kyrgyzstan's flag features a sun with 40 rays, representing the 40 tribes that united to form the country.",
        "The capital city of Kyrgyzstan is Bishkek."
    ],
    "Turkmenistan": [
        "Turkmenistan has a burning gas crater called the 'Door to Hell' that has been on fire since 1971.",
        "The capital city of Turkmenistan is Ashgabat."
    ],
    "Denmark": [
        "Denmark is where LEGO bricks were invented! The name LEGO means 'play well' in Danish.",
        "The capital city of Denmark is Copenhagen."
    ],
    "Singapore": [
        "Singapore is a city-state, meaning the whole country is just one city!",
        "Singapore has a famous hotel with a boat-shaped rooftop garden and pool called Marina Bay Sands."
    ],
    "Finland": [
        "Finland has 178,947 islands, the third most of any country in the world.",
        "The capital city of Finland is Helsinki."
    ],
    "Norway": [
        "Norway has 239,057 islands, the second most of any country in the world.",
        "In 2008, Norway knighted a penguin!"
    ],
    "Slovakia": [
        "Slovakia has the highest number of castles and chateaux per person in the world.",
        "The capital city of Slovakia is Bratislava."
    ],
    "Central African Republic": [
        "The capital city of the Central African Republic is Bangui.",
        "In this country, people use 2 official languages: French and Sango."
    ],
    "Costa Rica": [
        "Costa Rica has no army! It abolished its military in 1948.",
        "Costa Rica is home to over 500,000 different species of plants and animals."
    ],
    "Ireland": [
        "Ireland is called the 'Emerald Isle' because of its lush green countryside.",
        "The capital city of Ireland is Dublin."
    ],
    "Liberia": [
        "The capital city of Liberia is Monrovia.",
        "In Liberia, the official language is English, but there are over 20 other indigenous languages."
    ],
    "New Zealand": [
        "New Zealand was the first country in the world to give women the right to vote, in 1893.",
        "New Zealand is home to more sheep and cows than people.",
        "There are no snakes in New Zealand."
    ],
    "Oman": [
        "The capital city of Oman is Muscat.",
        "In Oman, the main official language is Arabic, but people also use English and Baluchi."
    ],
    "Kuwait": [
        "Kuwait has the strongest currency in the world, the Kuwaiti dinar.",
        "The capital city of Kuwait is Kuwait City."
    ],
    "Mauritania": [
        "Mauritania is one of the least densely populated countries in the world, with lots of empty desert.",
        "The capital city of Mauritania is Nouakchott."
    ],
    "Panama": [
        "The Panama Canal connects the Atlantic and Pacific Oceans, and over 14,000 ships pass through it each year.",
        "The capital city of Panama is Panama City."
    ],
    "Croatia": [
        "Croatia is home to the world's smallest town, Hum, which has only about 20 people.",
        "The capital city of Croatia is Zagreb."
    ],
    "Georgia": [
        "Georgia is considered the birthplace of wine, with wine-making dating back over 8,000 years.",
        "The capital city of Georgia is Tbilisi."
    ],
    "Eritrea": [
        "Eritrea has the most colorful and unique traditional coffee ceremony in the Horn of Africa.",
        "The capital city of Eritrea is Asmara."
    ],
    "Uruguay": [
        "Uruguay was the first country in the world to fully legalize marijuana.",
        "The capital city of Uruguay is Montevideo."
    ],
    "Mongolia": [
        "Mongolia is the most sparsely populated country in the world, with more horses than people.",
        "The capital city of Mongolia is Ulaanbaatar."
    ],
    "Bosnia and Herzegovina": [
        "Bosnia and Herzegovina is home to Europe's only remaining jungle.",
        "The capital city of Bosnia and Herzegovina is Sarajevo."
    ],
    "Puerto Rico": [
        "Puerto Rico is called the 'Island of Enchantment' because of its beautiful beaches and rainforests.",
        "The capital city of Puerto Rico is San Juan."
    ],
    "Armenia": [
        "Armenia was the first country in the world to make Christianity its official religion, way back in 301 AD.",
        "The capital city of Armenia is Yerevan."
    ],
    "Albania": [
        "Albania has over 173,000 bunkers left over from its communist past, scattered across the country.",
        "The capital city of Albania is Tirana."
    ],
    "Lithuania": [
        "Lithuania was the first Soviet republic to declare independence from the Soviet Union in 1990.",
        "The capital city of Lithuania is Vilnius."
    ],
    "Qatar": [
        "Qatar is one of the richest countries in the world because of its natural gas and oil.",
        "The capital city of Qatar is Doha."
    ],
    "Jamaica": [
        "Jamaica is the birthplace of reggae music, made famous by Bob Marley.",
        "The capital city of Jamaica is Kingston."
    ],
    "Moldova": [
        "Moldova is one of the least visited countries in the world.",
        "The capital city of Moldova is Chisinau."
    ],
    "Namibia": [
        "Namibia is home to the world's oldest desert, the Namib Desert.",
        "The capital city of Namibia is Windhoek."
    ],
    "Gambia": [
        "The Gambia is the smallest country in mainland Africa, only about 50 km wide at its widest point.",
        "The capital city of The Gambia is Banjul."
    ],
    "Botswana": [
        "Botswana produces the most diamonds in the world by value.",
        "The capital city of Botswana is Gaborone."
    ],
    "Gabon": [
        "Gabon is home to about 80% of Africa's gorillas.",
        "The capital city of Gabon is Libreville."
    ],
    "Lesotho": [
        "Lesotho is a country completely surrounded by South Africa, with no borders on the sea.",
        "The capital city of Lesotho is Maseru."
    ],
    "Slovenia": [
        "Slovenia has over 10,000 caves, and you can even take a train inside one of them.",
        "The capital city of Slovenia is Ljubljana."
    ],
    "Latvia": [
        "Latvia has one of the fastest internet connections in the world.",
        "The capital city of Latvia is Riga."
    ],
    "North Macedonia": [
        "North Macedonia is home to Lake Ohrid, one of the oldest and deepest lakes in Europe.",
        "The capital city of North Macedonia is Skopje."
    ],
    "Kosovo": [
        "Kosovo has the youngest population in Europe, with an average age of about 25.",
        "The capital city of Kosovo is Pristina."
    ],
    "Guinea-Bissau": [
        "The capital city of Guinea-Bissau is Bissau.",
        "In Guinea-Bissau, the official language is Portuguese, but almost everyone uses a language called Kriol to talk to friends."
    ],
    "Equatorial Guinea": [
        "Equatorial Guinea is the only country in Africa where Spanish is the official language.",
        "The capital city of Equatorial Guinea is Malabo."
    ],
    "Bahrain": [
        "Bahrain is an island nation made up of 33 small islands.",
        "The capital city of Bahrain is Manama."
    ],
    "Trinidad and Tobago": [
        "Trinidad and Tobago is the birthplace of steelpan drums, the only musical instrument invented in the 20th century.",
        "The capital city of Trinidad and Tobago is Port of Spain."
    ],
    "Estonia": [
        "Estonia is one of the greenest countries in Europe, with 52% of its land covered in forest.",
        "The capital city of Estonia is Tallinn."
    ],
    "Timor-Leste": [
        "Timor-Leste is one of the youngest countries in the world, becoming independent in 2002.",
        "The capital city of Timor-Leste is Dili."
    ],
    "Mauritius": [
        "Mauritius is the only place in the world where you can find the now-extinct dodo bird in history books.",
        "The capital city of Mauritius is Port Louis."
    ],
    "Cyprus": [
        "Cyprus is known as the island of Aphrodite, the Greek goddess of love, who was said to be born there.",
        "The capital city of Cyprus is Nicosia."
    ],
    "Eswatini": [
        "Eswatini is one of the last remaining absolute monarchies in the world.",
        "The capital city of Eswatini is Mbabane."
    ],
    "Djibouti": [
        "Djibouti is home to Lake Assal, the lowest point in Africa and the saltiest lake outside Antarctica.",
        "The capital city of Djibouti is Djibouti."
    ],
    "Fiji": [
        "Fiji has over 330 islands, but only about 100 of them are inhabited.",
        "The capital city of Fiji is Suva."
    ],
    "Comoros": [
        "Comoros is known as the 'Perfume Islands' because it grows many flowers used to make perfume.",
        "The capital city of Comoros is Moroni."
    ],
    "Guyana": [
        "Guyana is the only country in South America where English is the official language.",
        "The Kaieteur Falls in Guyana is one of the tallest single-drop waterfalls in the world."
    ],
    "Bhutan": [
        "Bhutan measures its success by 'Gross National Happiness' instead of just money.",
        "The capital city of Bhutan is Thimphu."
    ],
    "Solomon Islands": [
        "The Solomon Islands were named after King Solomon because it was believed he had mines of gold there.",
        "The capital city of the Solomon Islands is Honiara."
    ],
    "Luxembourg": [
        "Luxembourg is one of the smallest countries in Europe but one of the richest in the world.",
        "The capital city of Luxembourg is Luxembourg."
    ],
    "Montenegro": [
        "Montenegro means 'Black Mountain' in the local language.",
        "The capital city of Montenegro is Podgorica."
    ],
    "Suriname": [
        "Suriname is the smallest country in South America.",
        "The capital city of Suriname is Paramaribo."
    ],
    "Cabo Verde": [
        "Cabo Verde is a group of islands off the coast of West Africa.",
        "The capital city of Cabo Verde is Praia."
    ],
    "Malta": [
        "Malta is one of the smallest countries in the world but has the most historic sites per square kilometer.",
        "The capital city of Malta is Valletta."
    ],
    "Maldives": [
        "The Maldives is the lowest and flattest country in the world, with an average ground level of just 1.5 meters.",
        "The capital city of the Maldives is Male."
    ],
    "Brunei": [
        "Brunei is one of the few remaining countries in the world ruled by an absolute monarch, called a Sultan.",
        "The capital city of Brunei is Bandar Seri Begawan."
    ],
    "Belize": [
        "Belize is home to the Great Blue Hole, a giant underwater sinkhole that is visible from space.",
        "The capital city of Belize is Belmopan."
    ],
    "Bahamas": [
        "The Bahamas has over 700 islands, but only about 30 of them are inhabited.",
        "The capital city of the Bahamas is Nassau."
    ],
    "Iceland": [
        "Iceland has no mosquitoes at all, not even one!",
        "Icelanders drink more Coca-Cola per person than any other country in the world."
    ],
    "Vanuatu": [
        "Vanuatu is the birthplace of bungee jumping! Men fasten vines to their ankles and jump from tall wooden platforms.",
        "The capital city of Vanuatu is Port Vila."
    ],
    "Barbados": [
        "Barbados is the birthplace of rum, which was first made there in the 1600s.",
        "The capital city of Barbados is Bridgetown."
    ],
    "Samoa": [
        "Samoa has a third gender called fa'afafines, and people who are fa'afafine are fully accepted in society.",
        "The capital city of Samoa is Apia."
    ],
    "Saint Lucia": [
        "Saint Lucia is the only country in the world named after a woman, Saint Lucy.",
        "The capital city of Saint Lucia is Castries."
    ],
    "Guam": [
        "Guam is a tiny island territory of the United States in the Pacific Ocean.",
        "The capital city of Guam is Hagatna."
    ],
    "Kiribati": [
        "Kiribati is the only country in the world that is located in all four hemispheres at once.",
        "The capital city of Kiribati is South Tarawa."
    ],
    "Seychelles": [
        "Seychelles has some of the most beautiful beaches in the world, with pink sand on some islands.",
        "The capital city of Seychelles is Victoria."
    ],
    "Grenada": [
        "Grenada is known as the 'Island of Spice' because it grows lots of nutmeg and mace.",
        "The capital city of Grenada is Saint George's."
    ],
    "Tonga": [
        "Tonga is the only Pacific island nation that was never colonized by European powers.",
        "The capital city of Tonga is Nuku'alofa."
    ],
    "Micronesia": [
        "Micronesia is made up of over 600 islands in the Pacific Ocean.",
        "The capital city of Micronesia is Palikir."
    ],
    "Antigua and Barbuda": [
        "Antigua means 'ancient' in Spanish, and Barbuda means 'bearded'.",
        "The capital city of Antigua and Barbuda is Saint John's."
    ],
    "Andorra": [
        "Andorra is a tiny country between France and Spain.",
        "The capital city of Andorra is Andorra la Vella."
    ],
    "Dominica": [
        "Dominica is home to the Boiling Lake, the second-largest hot spring in the world.",
        "The capital city of Dominica is Roseau."
    ],
    "Cayman Islands": [
        "The Cayman Islands are famous for having more registered businesses than people.",
        "The capital city of the Cayman Islands is George Town."
    ],
    "Bermuda": [
        "Bermuda is famous for the Bermuda Triangle, an area where ships and planes have mysteriously disappeared.",
        "The capital city of Bermuda is Hamilton."
    ],
    "Greenland": [
        "Greenland is the world's largest island that is not a continent.",
        "The capital city of Greenland is Nuuk."
    ],
    "Faroe Islands": [
        "The Faroe Islands have more sheep than people.",
        "The capital city of the Faroe Islands is Torshavn."
    ],
    "Saint Kitts and Nevis": [
        "Saint Kitts and Nevis is the smallest country in the Americas by both area and population.",
        "The capital city of Saint Kitts and Nevis is Basseterre."
    ],
    "Monaco": [
        "Monaco is the second smallest country in the world but has the most millionaires per person.",
        "The capital city of Monaco is Monaco."
    ],
    "Liechtenstein": [
        "Liechtenstein is one of the smallest countries in the world and is located between Switzerland and Austria.",
        "The capital city of Liechtenstein is Vaduz."
    ],
    "San Marino": [
        "San Marino is one of the oldest republics in the world, founded in 301 AD.",
        "The capital city of San Marino is San Marino."
    ],
    "Gibraltar": [
        "Gibraltar is a British territory at the southern tip of Spain, famous for its Rock of Gibraltar.",
        "The capital city of Gibraltar is Gibraltar."
    ],
    "British Virgin Islands": [
        "The British Virgin Islands are a group of about 60 islands in the Caribbean.",
        "The capital city of the British Virgin Islands is Road Town."
    ],
    "Palau": [
        "The capital city of Palau is Ngerulmud.",
        "In Palau, people use 2 official languages, Palauan and English, but some islands also use Japanese."
    ],
    "Cook Islands": [
        "The Cook Islands are named after the British explorer Captain James Cook.",
        "The capital city of the Cook Islands is Avarua."
    ],
    "Anguilla": [
        "Anguilla is a British island territory known for its beautiful white sand beaches.",
        "The capital city of Anguilla is The Valley."
    ],
    "Tuvalu": [
        "The capital city of Tuvalu is Funafuti.",
        "In Tuvalu, people use 2 main languages: Tuvaluan and English."
    ],
    "Nauru": [
        "Nauru is a tiny island country in the Pacific Ocean.",
        "Nauru does not have an official capital city."
    ],
    "Saint Barthelemy": [
        "Saint Barthelemy is a French island in the Caribbean nicknamed 'St. Barts'.",
        "The capital city of Saint Barthelemy is Gustavia."
    ],
    "Saint Helena": [
        "Saint Helena is a remote volcanic island in the South Atlantic, famous as the place where Napoleon was exiled.",
        "The capital city of Saint Helena is Jamestown."
    ],
    "Montserrat": [
        "Montserrat is a Caribbean island with an active volcano that has destroyed its capital city twice.",
        "The capital city of Montserrat is Plymouth (abandoned) and Brades."
    ],
    "Falkland Islands": [
        "The Falkland Islands have about half a million sheep but only about 3,000 people.",
        "The capital city of the Falkland Islands is Stanley."
    ],
    "Niue": [
        "Niue is the world's first and only 'WIFI nation,' with free internet access across the whole country.",
        "The capital city of Niue is Alofi."
    ],
    "Tokelau": [
        "Tokelau is a territory of New Zealand made up of three small atolls in the Pacific.",
        "Tokelau runs almost entirely on solar power."
    ],
    "Vatican City": [
        "Vatican City is the smallest country in the world, smaller than many city parks.",
        "Vatican City has the highest amount of art per person in the world."
    ],
    "Hong Kong": [
        "Hong Kong has more skyscrapers than any other city in the world.",
        "Hong Kong is a Special Administrative Region of China."
    ],
    "French Polynesia": [
        "French Polynesia includes over 100 islands, the most famous being Tahiti and Bora Bora.",
        "The capital city of French Polynesia is Papeete."
    ],
    "New Caledonia": [
        "New Caledonia has one of the largest coral reef systems in the world, second only to Australia's Great Barrier Reef.",
        "The capital city of New Caledonia is Noumea."
    ]
}

# Capital cities for fallback
capitals = {
    "Yemen": "Sana'a", "Cuba": "Havana", "Austria": "Vienna", "Hungary": "Budapest",
    "Tajikistan": "Dushanbe", "Belarus": "Minsk", "Israel": "Jerusalem",
    "Switzerland": "Bern", "Togo": "Lome", "Sierra Leone": "Freetown",
    "Laos": "Vientiane", "Paraguay": "Asuncion", "Libya": "Tripoli",
    "Bulgaria": "Sofia", "Serbia": "Belgrade", "El Salvador": "San Salvador",
    "Nicaragua": "Managua", "Kyrgyzstan": "Bishkek", "Turkmenistan": "Ashgabat",
    "Denmark": "Copenhagen", "Singapore": "Singapore", "Finland": "Helsinki",
    "Norway": "Oslo", "Slovakia": "Bratislava", "Costa Rica": "San Jose",
    "Ireland": "Dublin", "New Zealand": "Wellington", "Kuwait": "Kuwait City",
    "Mauritania": "Nouakchott", "Panama": "Panama City", "Croatia": "Zagreb",
    "Georgia": "Tbilisi", "Eritrea": "Asmara", "Uruguay": "Montevideo",
    "Mongolia": "Ulaanbaatar", "Puerto Rico": "San Juan", "Armenia": "Yerevan",
    "Albania": "Tirana", "Lithuania": "Vilnius", "Qatar": "Doha",
    "Jamaica": "Kingston", "Moldova": "Chisinau", "Namibia": "Windhoek",
    "Gambia": "Banjul", "Botswana": "Gaborone", "Gabon": "Libreville",
    "Lesotho": "Maseru", "Slovenia": "Ljubljana", "Latvia": "Riga",
    "North Macedonia": "Skopje", "Kosovo": "Pristina", "Equatorial Guinea": "Malabo",
    "Bahrain": "Manama", "Trinidad and Tobago": "Port of Spain", "Estonia": "Tallinn",
    "Timor-Leste": "Dili", "Mauritius": "Port Louis", "Cyprus": "Nicosia",
    "Eswatini": "Mbabane", "Djibouti": "Djibouti", "Fiji": "Suva",
    "Comoros": "Moroni", "Bhutan": "Thimphu", "Solomon Islands": "Honiara",
    "Luxembourg": "Luxembourg", "Montenegro": "Podgorica", "Cabo Verde": "Praia",
    "Malta": "Valletta", "Maldives": "Male", "Brunei": "Bandar Seri Begawan",
    "Belize": "Belmopan", "Bahamas": "Nassau", "Vanuatu": "Port Vila",
    "Barbados": "Bridgetown", "Samoa": "Apia", "Saint Lucia": "Castries",
    "Guam": "Hagatna", "Kiribati": "South Tarawa", "Seychelles": "Victoria",
    "Grenada": "Saint George's", "Tonga": "Nuku'alofa", "Micronesia": "Palikir",
    "Antigua and Barbuda": "Saint John's", "Andorra": "Andorra la Vella",
    "Dominica": "Roseau", "Cayman Islands": "George Town", "Bermuda": "Hamilton",
    "Greenland": "Nuuk", "Faroe Islands": "Torshavn", "Saint Kitts and Nevis": "Basseterre",
    "Monaco": "Monaco", "Liechtenstein": "Vaduz", "San Marino": "San Marino",
    "Gibraltar": "Gibraltar", "British Virgin Islands": "Road Town",
    "Cook Islands": "Avarua", "Anguilla": "The Valley", "Saint Barthelemy": "Gustavia",
    "Saint Helena": "Jamestown", "Montserrat": "Brades", "Falkland Islands": "Stanley",
    "Niue": "Alofi", "French Polynesia": "Papeete", "New Caledonia": "Noumea"
}

# For countries not in facts_map, generate a simple fact
def generate_fallback(country_name):
    cap = capitals.get(country_name, f"{country_name}")
    return [f"The capital city of {country_name} is {cap}."]

output = []
for c in countries:
    name = c["country"]
    pop = c["population"]
    facts = facts_map.get(name, generate_fallback(name))
    output.append({
        "country": name,
        "population": pop,
        "facts": facts
    })

with open(os.path.join(BASE, 'facts.json'), 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Generated facts.json with {len(output)} countries.")
