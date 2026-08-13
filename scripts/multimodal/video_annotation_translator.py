import csv, sys

def main():
    src = r'd:/paramananda/annotations_by_clip.csv'
    eng_path = r'd:/paramananda/gpt_oss_english.csv'
    nep_path = r'd:/paramananda/gpt_oss_nepali.csv'
    # Read source
    with open(src, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    header = rows[0]
    data = rows[1:]
    # Predefined translations for first 10 rows
    batch_1_en = [
        ('There are supporting artists behind both sides of the lead singer.', 'While singing, the boys have started dancing.', 'Yellow lights are lit all around.', ''),
        ('There are cows and sheep around the hills.', 'A boy wearing a brown traditional dress is driving the sheep, and a beautiful girl is enjoying watching that scene.', 'Blue sky, greenery all around, large trees, and beautiful weather.', ''),
        ('In the center, the lead male artist and female artist are sitting together.', 'The lead couple is sitting in the middle, looking at each other while performing playfully.', 'Traditional utensils are seen on a large stone headboard-like platform.', ''),
        ('A beautiful woman dressed in a pink saree and in front of her, a man in white attire with a red turban tied on his head.', 'They are looking at each other, blushing and smiling with open hearts.', 'In a dim nighttime background, dancers wearing traditional Tharu attire and carrying burning oil lamps in their hands are dancing in circles around them.', ''),
        ('The girl is wearing a modern lehenga-style dress in a sky blue and white combination. Around her are beautiful white and colorful flower plants, and butterflies can also be seen swarming.', 'Sitting near the flowers in the meadow, the girl tries to catch a butterfly sitting on a white flower while lip-syncing to the song rhythm with hopeful expressions.', 'Green hilly landscape, open sky above, and a slightly dim view of a mountain village and hills on the side.', ''),
        ('Boy and girl', 'They are dancing holding handkerchiefs in their hands', 'Lights and background dancers are dancing', ''),
        ('Girl', 'The girl is talking', 'Mountains / Hills', ''),
        ('Boy and girl', 'Many people are dancing', 'There is a yellow wall and they are dancing', ''),
        ('A lead male character wearing a purple patterned kurta with a sash around his waist, and to his right, a lead female character wearing a choli, light yellow fariya (saree), and potey necklace around her neck.', 'The young man and the young woman swaying her waist are dancing playfully.', 'Lush green rural backdrop & supporting dancers wearing red choli and dark yellow fariya along with yellow potey around their necks.', ''),
        ('Girls are standing on the grass.', 'The girls are dancing.', 'There is a small stream near the green grass, and a forest in the background.', '')
    ]
    batch_1_ne = [
        ('मुख्य गायकको दुवैपट्टि पछाडि सह-कलाकारहरू छन्।', 'गाउँदागाउँदै केटाहरू नाच्न थालेका छन्।', 'चारैतिर पहेंलो बत्ती बलेको।', ''),
        ('पहाड वरिपरि गायवस्तु र भेडाहरू छन्।', 'खैरो रङको पहिरन पोसाक लगाएको केटाले भेडाहरूलाई धपाउँदै छ अनि एउटा सुन्दर केटीले त्यो दृश्य देखेर रमाउँदै छिन्।', 'नीलो आकाश, चारैतिर हरियाली, ठूला-ठूला रूख, र सुन्दर मौसम।', ''),
        ('बीचमा मुख्य कलाकार (केटा) र कलाकार (केटी) एकैसाथ बसेका छन्।', 'मुख्य जोडी बीचमा बसेर एक-अर्कालाई हेर्दै रमाइलो अभिनय गर्दै छन्।', 'ढुङ्गाले बनेको ठूलो सिरानी जस्तो ठाउँमा परम्परागत भाँडा देखिन्छ।', ''),
        ('गुलाबी साडीमा सजिएकी एक सुन्दरी महिला र उनको सामुन्ने सेतो पोसाकका साथै टाउकोमा रातो फेटा बाँधेका एक पुरुष।', 'एकअर्कालाई हेर्दै लजाएर खुला हृदयले मुस्कुराइरहेका छन्।', 'रात्रिकालीन धमिलो पृष्ठभूमिमा, परम्परागत थारु पोसाक लगाएका र हातमा बलिरहेको दियो बोकेका नर्तकीहरू उनीहरूलाई केन्द्रविन्दुमा राखी वरिपरि घुमदै नृत्य गरिरहेका छन्।', ''),
        ('केटीले आकाशी नीलो र सेतो संयोजनको आधुनिक लेहङ्गा-शैलीको पोसाक लगाएकी छिन्। उनका वरिपरि राम्रा सेता र रंगीन फूलका बोटहरू छन् र पुतली पनि झुम्मिएको देखिन्छ।', 'केटी चौरको फूलको छेउमा बसेर, एउटा सेतो फूलमाथि बसेको पुतलीलाई छोप्न खोज्दै अनि गीतको तालमा लिप-सिङ्क र आशामायी अभिव्यक्ति दिइरहेकी छिन्।', 'हरियो पहाडी भू-भाग, माथि खुला आकाश, र साइडमा थोरै धमिलो रूपमा पहाडी गाउँ र डाँडाहरू देखिन्छन्।', ''),
        ('केटा र केटी', 'हातमा रुमाल बोकेर नाचिरहेका छन्', 'लाइट अनि ब्याकग्राउन्ड डान्सर नाचिरहेका छन्', ''),
        ('केटी', 'केटी बोलिरहेकी छिन्', 'पहाड', ''),
        ('केटा र केटी', 'धेरै मानिसहरू नाचिरहेका छन्', 'पहेंलो भित्ता छ अनि नाचिरहेका छन्', ''),
        ('बैजनी बुट्टेदार कुर्ता र कम्मरमा पटुका बाँधेका एक मुख्य युवा पात्र र उनका दायाँतर्फ चोली, हल्का पहेंलो रङको फरिया र घाटीमा पोते लगाएकी एक मुख्य युवती पात्र।', 'ती युवा र कम्मर मर्काउँदै गरेकी युवती चञ्चल रूपमा नृत्य गरिरहेका।', 'हरियाली देखिने ग्रामीण भेगको पृष्ठभूमि र सहायक रूपमा रातो चोली र गाढा पहेंलो रङको फरियासँगै घाटीमा पहेंलो पोते लगाएका नर्तकीहरू.', ''),
        ('केटीहरू घाँसमाथि उभिएका छन्।', 'केटीहरू नाचिरहेका छन्।', 'हरियो घाँसको छेउमा सानो खोला छ भने पछाडि जङ्गल छ।', '')
    ]
    with open(eng_path, 'w', encoding='utf-8', newline='') as f_eng, open(nep_path, 'w', encoding='utf-8', newline='') as f_nep:
        writer_eng = csv.writer(f_eng)
        writer_nep = csv.writer(f_nep)
        writer_eng.writerow(header)
        writer_nep.writerow(header)
        for i, row in enumerate(data):
            eng_row = row[:]
            nep_row = row[:]
            if i < 10:
                sub_en, act_en, bg_en, note_en = batch_1_en[i]
                sub_ne, act_ne, bg_ne, note_ne = batch_1_ne[i]
                eng_row[2] = sub_en
                eng_row[3] = act_en
                eng_row[4] = bg_en
                eng_row[5] = note_en
                nep_row[2] = sub_ne
                nep_row[3] = act_ne
                nep_row[4] = bg_ne
                nep_row[5] = note_ne
            writer_eng.writerow(eng_row)
            writer_nep.writerow(nep_row)
    print('Created', eng_path, 'and', nep_path)

if __name__ == '__main__':
    main()
