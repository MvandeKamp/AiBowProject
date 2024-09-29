import matplotlib.pyplot as plt
import numpy as np

# Data
data = [0.03620596711036173, 0.036274294356263725, 0.03648755061425509, 0.03651573923125599, 0.03653836522546221, 0.036837417538898305, 0.03701958822064806, 0.036873926937663705, 0.036997226229336405, 0.036699489125710735, 0.03628235228535544, 0.03715866640292563, 0.03676996963287361, 0.03779938338345885, 0.03711870593385416, 0.0370432793047989, 0.03677323585524163, 0.03697575566998824, 0.03722350421119329, 0.03669091249299216, 0.03717788248651981, 0.03862593154574137, 0.03911149613340855, 0.0401253098020697, 0.045756970152051636, 0.04923991011724634, 0.04785759270423543, 0.04903669412160575, 0.048567143837626725, 0.04847668405870667, 0.05133155150591908, 0.053871403814335146, 0.0554036116190932, 0.059810717927431645, 0.05518664223441127, 0.0585131154138005, 0.057435000564633056, 0.058387609334005455, 0.052668233611539716, 0.0596120642356572, 0.05791217024998253, 0.05954747847558692, 0.05936868121817225, 0.05830653970561648, 0.06520074397688429, 0.06833270231250056, 0.06521428449645293, 0.07273178200272859, 0.06869299930848383, 0.06758872270321949, 0.06767191924288316, 0.07407810146364278, 0.07624116757271053, 0.07613503595015413, 0.0785719145631267, 0.07046670298723592, 0.07290456886045349, 0.07287966102228038, 0.07963483275057155, 0.08057661083950073, 0.08426616349130502, 0.08279559819819474, 0.08098733621031011, 0.08142543570774234, 0.08573210842727426, 0.09431371546406353, 0.08243161282394261, 0.08455159553392158, 0.09506770026361773, 0.08988057986955045, 0.08994198679598778, 0.10162973971967258, 0.08888223616934106, 0.09233312235997163, 0.09684882305620514, 0.09835141450604679, 0.09385598922753448, 0.10006561969573982, 0.08894986152244559, 0.09411296637896309, 0.0852409859371709, 0.0857026253413555, 0.08289036187140969, 0.07366443900455397, 0.0734432053319295, 0.08734978597656023, 0.07947792506942389, 0.08337619827644618, 0.07302326375805071, 0.07245716556236688, 0.06824120672990719, 0.07101930675949415, 0.07396065552079673, 0.07523923307162408, 0.07349655996360475, 0.07813926381336883, 0.08726156310345794, 0.07253327959425017, 0.07757463958352848, 0.07219599470854562, 0.07210498131566766, 0.07929184605195645, 0.07956086560612353, 0.07365748626680105, 0.07746991098691695, 0.08627883133707111, 0.07510659664392332, 0.07024192608453227, 0.0764449249143363]
stdev = [0.019312674877977807, 0.019365313076113545, 0.01835604854025135, 0.019121772498110867, 0.017939958810041526, 0.01999548509260339, 0.021279612518782028, 0.021058836501958462, 0.020733319070135876, 0.02024407224447295, 0.018952016615613743, 0.02140173782407514, 0.02044856517141887, 0.023159869632879887, 0.020820555103655863, 0.021430820563350304, 0.01998706801273111, 0.02136420138210559, 0.02086565943740106, 0.018676956926142834, 0.021041052256079888, 0.023785328675901534, 0.023144156232963887, 0.024652440611858516, 0.05619679411030314, 0.05810722185933107, 0.05990218575976942, 0.06027048495099905, 0.05951734677974324, 0.0614886459080206, 0.06226501925499804, 0.056324215036800185, 0.06882593728430635, 0.07514555076558307, 0.07319506308501629, 0.07465397179589624, 0.07085900812124862, 0.07656949848386885, 0.07339388312141967, 0.06954833804529603, 0.07231921904015222, 0.0718086699661846, 0.07518264094838896, 0.06682855603917878, 0.07394413068133487, 0.08223413511778618, 0.08130209987753056, 0.08482089721833716, 0.07872682772471927, 0.0741000445846516, 0.08122076469054472, 0.09318723010246731, 0.0912660522827497, 0.09521622040721844, 0.10404103769979911, 0.08954462453752632, 0.09518466310831164, 0.09511346427942084, 0.10524970038141067, 0.09829683647061084, 0.10463516715227715, 0.09452985190258785, 0.09713383039920756, 0.09863368642823248, 0.10024703597942722, 0.11176778978941894, 0.1020063348646967, 0.10110480746170976, 0.11105523431353177, 0.1044442067934858, 0.10502818558786518, 0.10728020148426642, 0.10966888176744234, 0.11983693973926925, 0.13047200674946077, 0.11508340993036031, 0.11764611910273272, 0.12177912445910635, 0.10841744461692311, 0.11961323193356437, 0.10543168984624395, 0.09974054913393081, 0.09402432469197887, 0.09657734600921364, 0.09284398921534104, 0.10634400293850453, 0.09098076793744547, 0.1027995547516878, 0.08949073525564806, 0.09807529648967525, 0.10103306669892936, 0.09761752931347849, 0.10710545923224803, 0.11704651123793329, 0.1138614092315351, 0.11106053526344332, 0.1302881134360724, 0.10888458738941541, 0.11021306855823, 0.10537725880566622, 0.09904710550320836, 0.11317827983376101, 0.11095838982467461, 0.10386706029402704, 0.10765183912992012, 0.11972844962484745, 0.1094921312342357, 0.10485023313937984, 0.11264652336128717]

# X-axis values
x = np.arange(len(data))

# Plot
plt.figure(figsize=(10, 5))
plt.errorbar(x, data, yerr=stdev, fmt='-o', ecolor='r', capsize=3, label='Mean with Std Dev')
plt.title('Fitness Duchschnitt mit Standardabweichung')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.tight_layout()
plt.legend()
plt.grid(True)
plt.show()