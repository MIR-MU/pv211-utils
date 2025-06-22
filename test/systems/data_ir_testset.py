from collections import OrderedDict
from pv211_utils.entities import DocumentBase, QueryBase


class TestDocument(DocumentBase):
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text


class TestQuery(QueryBase):
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text


DOCUMENTS = OrderedDict({
    "1": TestDocument(
        "Beekeeping, also known as apiculture, is the maintenance of bee "
        "colonies, commonly in man-made hives."
    ),
    "2": TestDocument(
        "A primary challenge in beekeeping is managing the Varroa destructor "
        "mite, a parasite that weakens bees."
    ),
    "3": TestDocument(
        "The annual honey harvest is a key reward of beekeeping, requiring "
        "careful extraction and processing."
    ),
    "4": TestDocument(
        "The Roman Republic was characterized by a constitution centered on "
        "the principles of a separation of powers and checks and balances."
    ),
    "5": TestDocument(
        "The Colosseum in Rome, Italy, is an elliptical amphitheatre, the "
        "largest ever built."
    ),
    "6": TestDocument(
        "Roman legions were known for their disciplined infantry tactics, "
        "such as the testudo formation."
    ),
    "7": TestDocument(
        "Sourdough bread is made by the fermentation of dough using naturally "
        "occurring lactobacilli and yeast."
    ),
    "8": TestDocument(
        "Python's design philosophy emphasizes code readability with its "
        "notable use of significant indentation."
    ),
    "9": TestDocument(
        "The Great Barrier Reef, located off the coast of Australia, is the "
        "world's largest coral reef system."
    ),
    "10": TestDocument(
        "Scuba diving allows humans to explore underwater environments by "
        "using a self-contained underwater breathing apparatus."
    ),
    "11": TestDocument(
        "A VIN, or Vehicle Identification Number, is a unique code used by "
        "the automotive industry to identify individual motor vehicles."
    ),
    "12": TestDocument(
        "The CPU, or Central Processing Unit, is the electronic circuitry "
        "that executes instructions comprising a computer program."
    ),
    "13": TestDocument(
        "Fresco is a technique of mural painting executed upon freshly laid, "
        "or wet lime plaster."
    ),
    "14": TestDocument(
        "A glacier is a persistent body of dense ice that is constantly "
        "moving under its own weight."
    ),
    "15": TestDocument(
        "The concept of a 'bond' in finance is an instrument of indebtedness "
        "of the bond issuer to the holders."
    ),
    "16": TestDocument(
        "Espresso is a coffee-brewing method of Italian origin, in which a "
        "small amount of nearly boiling water is forced under pressure."
    ),
    "17": TestDocument(
        "The king cobra is a species of venomous elapid snake endemic to "
        "jungles in Southern and Southeast Asia."
    ),
    "18": TestDocument(
        "Foraging for wild mushrooms requires expert knowledge, as many "
        "species are poisonous."
    ),
    "19": TestDocument(
        "Origami is the Japanese art of paper folding, which is often "
        "associated with Japanese culture."
    ),
    "20": TestDocument(
        "A firewall is a network security system that monitors and controls "
        "incoming and outgoing network traffic."
    ),
    "21": TestDocument(
        "The bumblebee is a large, hairy bee belonging to the genus Bombus."
    ),
    "22": TestDocument(
        "The character of James Bond was created by writer Ian Fleming in "
        "1953."
    ),
    "23": TestDocument(
        "The legion is a large unit in some national armies."
    ),
    "24": TestDocument(
        "Gardening is the practice of growing and cultivating plants as part "
        "of horticulture."
    ),
    "25": TestDocument(
        "Soil composition is vital for healthy gardening; it should contain a "
        "mix of clay, sand, and silt."
    ),
    "26": TestDocument(
        "Pruning is a horticultural practice involving the selective removal "
        "of parts of a plant, such as branches or buds."
    ),
    "27": TestDocument(
        "A carburetor is a device that blends air and fuel for an internal "
        "combustion engine."
    ),
    "28": TestDocument(
        "The Andes is the longest continental mountain range in the world, "
        "forming a continuous highland along the western edge of South "
        "America."
    ),
    "29": TestDocument(
        "Mycology is the branch of biology concerned with the study of fungi."
    ),
    "30": TestDocument(
        "A loom is a device used to weave cloth and tapestry."
    ),
})


TRIVIAL_TEST_CASES = [
    {"test_name": "Unique 'apiculture'",
     "query": TestQuery("Beekeeping"), "expected_doc_in_top_3": "2"},
    {"test_name": "Unique 'VIN'",
     "query": TestQuery("automotive VIN code"), "expected_doc_in_top_3": "11"},
    {"test_name": "Unique 'CPU'",
     "query": TestQuery("Central Processing Unit circuitry"),
     "expected_doc_in_top_3": "12"},
    {"test_name": "Unique 'Fresco'",
     "query": TestQuery("fresco mural painting plaster"),
     "expected_doc_in_top_3": "13"},
    {"test_name": "Unique 'Glacier'",
     "query": TestQuery("persistent dense ice glacier"),
     "expected_doc_in_top_3": "14"},
    {"test_name": "Unique 'Origami'",
     "query": TestQuery("japanese art paper folding origami"),
     "expected_doc_in_top_3": "19"},
    {"test_name": "Unique 'Loom'",
     "query": TestQuery("weave cloth tapestry loom"),
     "expected_doc_in_top_3": "30"},
    {"test_name": "Unique 'Carburetor'",
     "query": TestQuery("carburetor internal combustion"),
     "expected_doc_in_top_3": "27"},
    {"test_name": "Unique 'Mycology'",
     "query": TestQuery("mycology branch of biology fungi"),
     "expected_doc_in_top_3": "29"},
    {"test_name": "Unique 'Andes'",
     "query": TestQuery("Andes continental mountain range"),
     "expected_doc_in_top_3": "28"},
]


ADVANCED_TEST_CASES = [
    {"test_name": "General Beekeeping Query",
     "query": TestQuery("information about beekeeping"),
     "expected_doc_in_top_3": "1"},
    {"test_name": "General Rome Query",
     "query": TestQuery("facts about ancient Rome"),
     "expected_doc_in_top_3": "4"},
    {"test_name": "General Gardening Query",
     "query": TestQuery("how to start a garden"),
     "expected_doc_in_top_3": "24"},
    {"test_name": "Disambiguate Financial Bond",
     "query": TestQuery("government bond investment"),
     "expected_doc_in_top_3": "15", "must_exclude": ["22"]},
    {"test_name": "Disambiguate Bee Type",
     "query": TestQuery("bee colony maintenance"),
     "expected_doc_in_top_3": "1", "must_exclude": ["21"]},
    {"test_name": "Disambiguate Legion Type",
     "query": TestQuery("roman army legion tactics"),
     "expected_doc_in_top_3": "6", "must_exclude": ["23"]},
    {"test_name": "Include Beekeeping Cluster",
     "query": TestQuery("all about managing bee colonies"),
     "must_include_in_top_5": ["1", "2", "3"]},
    {"test_name": "Include Rome Cluster",
     "query": TestQuery("the Roman empire"),
     "must_include_in_top_5": ["4", "5", "6"]},
    {"test_name": "Include Gardening Cluster",
     "query": TestQuery("techniques for plant cultivation"),
     "must_include_in_top_5": ["24", "25", "26"]},
    {"test_name": "Semantic Query for CPU",
     "query": TestQuery("the brain of a computer"),
     "expected_doc_in_top_3": "12"},
]
