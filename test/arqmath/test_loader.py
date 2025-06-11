import unittest

from pv211_utils.arqmath.loader import (
    load_queries,
    load_questions,
    load_answers,
    load_judgements,
)


CACHE_DOWNLOAD = False

NUM_QUERIES_2020 = 77
NUM_QUERIES_2021 = 100
NUM_QUERIES_2022 = 100

QUERY_2020_ID = 1
QUERY_2020_TAGS = ["functions"]

QUERY_2021_ID = 201
QUERY_2021_TAGS = ["abstract-algebra", "matrices", "ring-theory"]

QUERY_2022_ID = 301
QUERY_2022_TAGS = [
    "linear-algebra",
    "matrices",
    "inequality",
    "norm",
    "holder-inequality",
]

QUESTION_ID = "614561"
QUESTION_TITLE = r"random thought: are some infinite sets larger than other"
QUESTION_UPVOTES = 3
QUESTION_VIEWS = 326
QUESTION_TAGS = ["infinity"]
QUESTION_ANSWER_DOCUMENT_IDS = ["614568", "614563", "614564", "614565"]

ANSWER_ID = "1199811"
ANSWER_UPVOTES = 1
ANSWER_IS_ACCEPTED = True

HIGH_RELEVANCE_TRAIN_2020 = (13, "563024")
MEDIUM_RELEVANCE_VALIDATION_2020 = (24, "1758902")
LOW_RELEVANCE_TEST_2020 = (16, "1002519")
NO_RELEVANCE_2020 = (40, "2106624")
NO_RELEVANCE_JUDGEMENT_2020 = (53, "377998")

HIGH_RELEVANCE_2021 = (206, "1898375")
MEDIUM_RELEVANCE_2021 = (283, "2355423")
LOW_RELEVANCE_2021 = (300, "626996")
NO_RELEVANCE_2021 = (285, "692754")
NO_RELEVANCE_JUDGEMENT_2021 = (249, "2587440")

ANSWER_IDS = set(
    QUESTION_ANSWER_DOCUMENT_IDS
    + [
        ANSWER_ID,
        HIGH_RELEVANCE_TRAIN_2020[1],
        MEDIUM_RELEVANCE_VALIDATION_2020[1],
        LOW_RELEVANCE_TEST_2020[1],
        NO_RELEVANCE_2020[1],
        NO_RELEVANCE_JUDGEMENT_2020[1],
        HIGH_RELEVANCE_2021[1],
        MEDIUM_RELEVANCE_2021[1],
        LOW_RELEVANCE_2021[1],
        NO_RELEVANCE_2021[1],
        NO_RELEVANCE_JUDGEMENT_2021[1],
    ]
)
ANSWERS_TEXT = load_answers(
    "text", cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS
)
ANSWERS_TEXT_LATEX = load_answers(
    "text+latex", cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS
)
ANSWERS_TEXT_PREFIX = load_answers(
    "text+prefix", cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS
)
ANSWERS_TEXT_TANGENTL = load_answers(
    "text+tangentl", cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS
)
ANSWERS_XHTML_LATEX = load_answers(
    "xhtml+latex", cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS
)
ANSWERS_XHTML_CMML = load_answers(
    "xhtml+cmml", cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS
)
ANSWERS_XHTML_PMML = load_answers(
    "xhtml+pmml", cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS
)


QUESTION_IDS = set(
    [
        QUESTION_ID,
    ]
)
QUESTIONS_TEXT = load_questions(
    "text",
    ANSWERS_TEXT,
    cache_download=CACHE_DOWNLOAD,
    filter_document_ids=QUESTION_IDS,
)
QUESTIONS_TEXT_LATEX = load_questions(
    "text+latex",
    ANSWERS_TEXT_LATEX,
    cache_download=CACHE_DOWNLOAD,
    filter_document_ids=QUESTION_IDS,
)
QUESTIONS_TEXT_TANGENTL = load_questions(
    "text+tangentl",
    ANSWERS_TEXT_TANGENTL,
    cache_download=CACHE_DOWNLOAD,
    filter_document_ids=QUESTION_IDS,
)
QUESTIONS_TEXT_PREFIX = load_questions(
    "text+prefix",
    ANSWERS_TEXT_PREFIX,
    cache_download=CACHE_DOWNLOAD,
    filter_document_ids=QUESTION_IDS,
)
QUESTIONS_XHTML_LATEX = load_questions(
    "xhtml+latex",
    ANSWERS_XHTML_LATEX,
    cache_download=CACHE_DOWNLOAD,
    filter_document_ids=QUESTION_IDS,
)
QUESTIONS_XHTML_CMML = load_questions(
    "xhtml+cmml",
    ANSWERS_XHTML_CMML,
    cache_download=CACHE_DOWNLOAD,
    filter_document_ids=QUESTION_IDS,
)
QUESTIONS_XHTML_PMML = load_questions(
    "xhtml+pmml",
    ANSWERS_XHTML_PMML,
    cache_download=CACHE_DOWNLOAD,
    filter_document_ids=QUESTION_IDS,
)


class TestLoadQueriesText(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries("text", subset=None, year=2020)
        self.queries_2021 = load_queries("text", subset=None, year=2021)
        self.queries_2022 = load_queries("text", subset=None, year=2022)

        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]
        self.query_2022 = self.queries_2022[QUERY_2022_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))
        self.assertEqual(NUM_QUERIES_2022, len(self.queries_2022))

    def test_query_title(self):
        self.assertIn(r"Finding value of  such that", self.query_2020.title)
        self.assertEqual(
            r"Matrix over division ring having one sided inverse is invertible",
            self.query_2021.title,
        )
        self.assertEqual(
            r"Inequality between norm 1,norm 2 and norm  of Matrices",
            self.query_2022.title,
        )

    def test_query_body(self):
        self.assertIn(r"If  then find the value of  ", self.query_2020.body)
        self.assertIn(r"If an  matrix over a division ring", self.query_2021.body)
        self.assertIn(r"Suppose  is a  matrix.", self.query_2022.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)
        self.assertEqual(QUERY_2022_TAGS, self.query_2022.tags)


class TestLoadQueriesLaTeX(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries("text+latex", subset=None, year=2020)
        self.queries_2021 = load_queries("text+latex", subset=None, year=2021)
        self.queries_2022 = load_queries("text+latex", subset=None, year=2022)

        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]
        self.query_2022 = self.queries_2022[QUERY_2022_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))
        self.assertEqual(NUM_QUERIES_2022, len(self.queries_2022))

    def test_query_title(self):
        self.assertIn(r"Finding value of $c$ such that", self.query_2020.title)
        self.assertEqual(
            r"Matrix over division ring having one sided inverse is invertible",
            self.query_2021.title,
        )
        self.assertEqual(
            r"Inequality between norm 1,norm 2 and norm $\infty$ of Matrices",
            self.query_2022.title,
        )

    def test_query_body(self):
        self.assertIn(
            r"If $f(x)= \frac{x^2 + x + c}{x^2 + 2x + c}$ then find the value of $c$",
            self.query_2020.body,
        )
        self.assertIn(
            r"If an $n\times n$ matrix over a division ring", self.query_2021.body
        )
        self.assertIn(r"Suppose $A$ is a $m\times n$ matrix.", self.query_2022.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)
        self.assertEqual(QUERY_2022_TAGS, self.query_2022.tags)


class TestLoadQueriesTangentL(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries("text+tangentl", subset=None, year=2020)
        self.queries_2021 = load_queries("text+tangentl", subset=None, year=2021)
        self.queries_2022 = load_queries("text+tangentl", subset=None, year=2022)

        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]
        self.query_2022 = self.queries_2022[QUERY_2022_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))
        self.assertEqual(NUM_QUERIES_2022, len(self.queries_2022))

    def test_query_title(self):
        self.assertIn(
            r"Finding value of #(start)# #(v!c,!0,-)# #(v!c,!0)# #(end)# such that",
            self.query_2020.title,
        )
        self.assertEqual(
            r"Matrix over division ring having one sided inverse is invertible",
            self.query_2021.title,
        )
        self.assertEqual(
            r"Inequality between norm 1,norm 2 and norm #(start)# #(v!∞,!0,-)# "
            "#(v!∞,!0)# #(end)# of Matrices",
            self.query_2022.title,
        )

    def test_query_body(self):
        self.assertIn(
            r"If #(start)# #(v!f,m!()1x1,n,-)# #(v!f,m!()1x1,n)# #(m!()1x1,[n,w],n)# "
            r"#(m!()1x1,[n,w])# #(m!()1x1,=,n,n)# #(m!()1x1,=,n)# #(=,f!,n,nn)# "
            r"#(=,f!,n)# #(f!,[o,u],nnn)# #(f!,[o,u])# #(f!,v!x,o,nnn)# #(f!,v!x,o)# "
            r"#(v!x,[n,a],nnno)# #(v!x,[n,a])# #(v!x,+,n,nnno)# #(v!x,+,n)# "
            r"#(+,v!x,n,nnnon)# #(+,v!x,n)# #(v!x,+,n,3n1o2n)# #(v!x,+,n)# "
            r"#(+,v!c,n,3n1o3n)# #(+,v!c,n)# #(v!c,!0,3n1o4n)# #(v!c,!0)# #{+,nn,nnnon}# "
            r"#{+,nn}# #(v!x,n!2,a,nnno)# #(v!x,n!2,a)# #(n!2,!0,nnnoa)# #(n!2,!0)# "
            r"#{v!x,nn,nnno}# #{v!x,nn}# #(f!,v!x,u,nnn)# #(f!,v!x,u)# #(v!x,[n,a],nnnu)# "
            r"#(v!x,[n,a])# #(v!x,+,n,nnnu)# #(v!x,+,n)# #(+,n!2,n,nnnun)# #(+,n!2,n)# "
            r"#(n!2,v!x,n,3n1u2n)# #(n!2,v!x,n)# #(v!x,+,n,3n1u3n)# #(v!x,+,n)# "
            r"#(+,v!c,n,3n1u4n)# #(+,v!c,n)# #(v!c,!0,3n1u5n)# #(v!c,!0)# "
            r"#{v!c,onnnn,1u5n,nnn}# #{v!c,onnnn,1u5n}# #{+,onnn,unnnn,nnn}# "
            r"#{+,onnn,unnnn}# #{+,on,unnnn,nnn}# #{+,on,unnnn}# #{v!x,onn,unnn,nnn}# "
            r"#{v!x,onn,unnn}# #{v!x,o,unnn,nnn}# #{v!x,o,unnn}# #{n!2,oa,unn,nnn}# "
            r"#{n!2,oa,unn}# #{+,onnn,un,nnn}# #{+,onnn,un}# #{+,on,un,nnn}# #{+,on,un}# "
            r"#{+,nnn,nnnun}# #{+,nnn}# #(v!x,n!2,a,nnnu)# #(v!x,n!2,a)# #(n!2,!0,nnnua)# "
            r"#(n!2,!0)# #{n!2,oa,ua,nnn}# #{n!2,oa,ua}# #{n!2,nn,a,nnnu}# #{n!2,nn,a}# "
            r"#{v!x,onn,u,nnn}# #{v!x,onn,u}# #{v!x,o,u,nnn}# #{v!x,o,u}# "
            r"#{v!x,nnn,nnnu}# #{v!x,nnn}# #(m!()1x1,v!x,w,n)# #(m!()1x1,v!x,w)# "
            r"#(v!x,!0,nw)# #(v!x,!0)# #{v!x,nnonn,w,n}# #{v!x,nnonn,w}# #{v!x,nno,w,n}# "
            r"#{v!x,nno,w}# #{v!x,2n1u3n,w,n}# #{v!x,2n1u3n,w}# #{v!x,nnu,w,n}# "
            r"#{v!x,nnu,w}# #(end)# then find the value of #(start)# #(v!c,!0,-)# "
            r"#(v!c,!0)# #(end)#",
            self.query_2020.body,
        )
        self.assertIn(
            r"If an #(start)# #(v!n,×,n,-)# #(v!n,×,n)# #(×,v!n,n,n)# #(×,v!n,n)# "
            r"#(v!n,!0,nn)# #(v!n,!0)# #{v!n,nn,-}# #{v!n,nn}# #(end)# matrix over a "
            r"division ring",
            self.query_2021.body,
        )
        self.assertIn(
            r"Suppose #(start)# #(v!a,!0,-)# #(v!a,!0)# #(end)# is a "
            r"#(start)# #(v!m,×,n,-)# #(v!m,×,n)# #(×,v!n,n,n)# #(×,v!n,n)# #(v!n,!0,nn)# "
            r"#(v!n,!0)# #(end)# matrix.",
            self.query_2022.body,
        )

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)
        self.assertEqual(QUERY_2022_TAGS, self.query_2022.tags)


class TestLoadQueriesPrefix(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries("text+prefix", subset=None, year=2020)
        self.queries_2021 = load_queries("text+prefix", subset=None, year=2021)
        self.queries_2022 = load_queries("text+prefix", subset=None, year=2022)

        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]
        self.query_2022 = self.queries_2022[QUERY_2022_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))
        self.assertEqual(NUM_QUERIES_2022, len(self.queries_2022))

    def test_query_title(self):
        self.assertIn(r"Finding value of V!𝑐 such that", self.query_2020.title)
        self.assertEqual(
            r"Matrix over division ring having one sided inverse is invertible",
            self.query_2021.title,
        )
        self.assertEqual(
            r"Inequality between norm 1,norm 2 and norm C!infinity of Matrices",
            self.query_2022.title,
        )

    def test_query_body(self):
        expected_body_2020 = (
            r"If U!eq U!times V!𝑓 V!𝑥 O!divide U!plus O!SUP V!𝑥 N!2 V!𝑥 V!𝑐 U!plus O!SUP V!𝑥 N!2 U!times N!2 V!𝑥 "
            r"V!𝑐 then find the value of V!𝑐"
        )
        self.assertIn(expected_body_2020, self.query_2020.body)

        self.assertIn(
            r"If an U!times V!𝑛 V!𝑛 matrix over a division ring", self.query_2021.body
        )
        self.assertIn(r"Suppose V!𝐴 is a U!times V!𝑚 V!𝑛 matrix.", self.query_2022.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)
        self.assertEqual(QUERY_2022_TAGS, self.query_2022.tags)


class TestLoadQueriesXHTMLLaTeX(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries("xhtml+latex", subset=None, year=2020)
        self.queries_2021 = load_queries("xhtml+latex", subset=None, year=2021)
        self.queries_2022 = load_queries("xhtml+latex", subset=None, year=2022)

        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]
        self.query_2022 = self.queries_2022[QUERY_2022_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))
        self.assertEqual(NUM_QUERIES_2022, len(self.queries_2022))

    def test_query_title(self):
        self.assertIn(
            r'Finding value of <span class="math-container" id="q_1">$c$</span> such that',
            self.query_2020.title,
        )
        self.assertEqual(
            r"Matrix over division ring having one sided inverse is invertible",
            self.query_2021.title,
        )
        self.assertEqual(
            r'Inequality between norm 1,norm 2 and norm <span class="math-container" '
            r'id="q_1">$\infty$</span> of Matrices',
            self.query_2022.title,
        )

    def test_query_body(self):
        expected_body_2020 = (
            r'<p>If <span class="math-container" id="q_4">$$f(x)= \frac{x^2 + x + c}{x^2 + 2x + c}$$</span> then '
            r'find the value of <span class="math-container" id="q_5">$c$</span>'
        )
        self.assertIn(expected_body_2020, self.query_2020.body)

        expected_body_2021 = (
            r'<p><em>If an <span class="math-container" id="q_1">$n\times n$</span> matrix over '
            r"a division ring"
        )
        self.assertIn(expected_body_2021, self.query_2021.body)

        expected_body_2022 = (
            r'<p>Suppose <span class="math-container" id="q_2">$A$</span> is a '
            r'<span class="math-container" id="q_3">$m\times n$</span> matrix.</p>'
        )
        self.assertIn(expected_body_2022, self.query_2022.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)
        self.assertEqual(QUERY_2022_TAGS, self.query_2022.tags)


class TestLoadQueriesXHTMLCMML(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries("xhtml+cmml", subset=None, year=2020)
        self.queries_2021 = load_queries("xhtml+cmml", subset=None, year=2021)
        self.queries_2022 = load_queries("xhtml+cmml", subset=None, year=2022)

        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]
        self.query_2022 = self.queries_2022[QUERY_2022_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))
        self.assertEqual(NUM_QUERIES_2022, len(self.queries_2022))

    def test_query_title(self):
        self.assertIn(
            r'<p>Finding value of <math xmlns="http://www.w3.org/1998/Math/MathML" '
            r'alttext="c" display="block"> <ci>𝑐</ci> </math> such that',
            self.query_2020.title,
        )
        self.assertEqual(
            r"<p>Matrix over division ring having one sided inverse is invertible</p>",
            self.query_2021.title,
        )
        self.assertEqual(
            r"<p>Inequality between norm 1,norm 2 and norm <math "
            r'xmlns="http://www.w3.org/1998/Math/MathML" encoding="MathML-Content">'
            r"<infinity/></math> of Matrices</p>",
            self.query_2022.title,
        )

    def test_query_body(self):
        expected_body_2020 = (
            r'If <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="f(x)=\frac{x^{2}+x+c}{x^{2}+2x+c}" '
            r'display="block"> <apply> <eq/> <apply> <times/> <ci>𝑓</ci> <ci>𝑥</ci> </apply> <apply> <divide/> <apply> '
            r'<plus/> <apply> <csymbol cd="ambiguous">superscript</csymbol> <ci>𝑥</ci> <cn type="integer">2</cn> '
            r'</apply> <ci>𝑥</ci> <ci>𝑐</ci> </apply> <apply> <plus/> <apply> <csymbol cd="ambiguous">superscript'
            r'</csymbol> <ci>𝑥</ci> <cn type="integer">2</cn> </apply> <apply> <times/> <cn type="integer">2</cn> '
            r"<ci>𝑥</ci> </apply> <ci>𝑐</ci> </apply> </apply> </apply> </math> then find the value of "
            r'<math xmlns="http://www.w3.org/1998/Math/MathML" alttext="c" display="block"> <ci>𝑐</ci> </math>'
        )
        self.assertIn(expected_body_2020, self.query_2020.body)

        expected_body_2021 = (
            r'<p><em>If an <math xmlns="http://www.w3.org/1998/Math/MathML" encoding="MathML-Content">'
            r"<apply><times/><ci>𝑛</ci><ci>𝑛</ci></apply></math> matrix over a division ring"
        )
        self.assertIn(expected_body_2021, self.query_2021.body)

        expected_body_2022 = (
            r'<p>Suppose <math xmlns="http://www.w3.org/1998/Math/MathML" encoding="MathML-Content"><ci>𝐴'
            r'</ci></math> is a <math xmlns="http://www.w3.org/1998/Math/MathML" encoding="MathML-Content">'
            r"<apply><times/><ci>𝑚</ci><ci>𝑛</ci></apply></math> matrix.</p>"
        )
        self.assertIn(expected_body_2022, self.query_2022.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)
        self.assertEqual(QUERY_2022_TAGS, self.query_2022.tags)


class TestLoadQueriesXHTMLPMML(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries("xhtml+pmml", subset=None, year=2020)
        self.queries_2021 = load_queries("xhtml+pmml", subset=None, year=2021)
        self.queries_2022 = load_queries("xhtml+pmml", subset=None, year=2022)

        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]
        self.query_2022 = self.queries_2022[QUERY_2022_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))
        self.assertEqual(NUM_QUERIES_2022, len(self.queries_2022))

    def test_query_title(self):
        self.assertIn(
            r'<p>Finding value of <math xmlns="http://www.w3.org/1998/Math/MathML" '
            r'alttext="c" display="block"> <mi>c</mi> </math> such that',
            self.query_2020.title,
        )
        self.assertEqual(
            r"<p>Matrix over division ring having one sided inverse is invertible</p>",
            self.query_2021.title,
        )
        self.assertEqual(
            r"<p>Inequality between norm 1,norm 2 and norm <math "
            r'xmlns="http://www.w3.org/1998/Math/MathML" alttext="\infty" '
            r'class="ltx_Math" display="block"><mi mathvariant="normal">∞</mi></math> '
            r"of Matrices</p>",
            self.query_2022.title,
        )

    def test_query_body(self):
        expected_body_2020 = (
            r'<math xmlns="http://www.w3.org/1998/Math/MathML" alttext="f(x)=\frac{x^{2}+x+c}{x^{2}+2x+c}" '
            r'display="block"> <mrow> <mrow> <mi>f</mi> <mo>⁢</mo> <mrow> <mo stretchy="false">(</mo> <mi>x</mi> '
            r'<mo stretchy="false">)</mo> </mrow> </mrow> <mo>=</mo> <mfrac> <mrow> <msup> <mi>x</mi> <mn>2</mn> '
            r"</msup> <mo>+</mo> <mi>x</mi> <mo>+</mo> <mi>c</mi> </mrow> <mrow> <msup> <mi>x</mi> <mn>2</mn> </msup> "
            r"<mo>+</mo> <mrow> <mn>2</mn> <mo>⁢</mo> <mi>x</mi> </mrow> <mo>+</mo> <mi>c</mi> </mrow> </mfrac> "
            r'</mrow> </math> then find the value of <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="c" '
            r'display="block"> <mi>c</mi> </math>'
        )
        self.assertIn(expected_body_2020, self.query_2020.body)

        expected_body_2021 = (
            r'<p><em>If an <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="n\times n" '
            r'class="ltx_Math" display="inline"><mrow><mi>n</mi><mo>×</mo><mi>n</mi></mrow></math> '
            r"matrix over a division ring"
        )
        self.assertIn(expected_body_2021, self.query_2021.body)

        expected_body_2022 = (
            r'<p>Suppose <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="A" class="ltx_Math" '
            r'display="block"><mi>A</mi></math> is a <math xmlns="http://www.w3.org/1998/Math/MathML" '
            r'alttext="m\times n" class="ltx_Math" display="block"><mrow><mi>m</mi><mo>×</mo><mi>n</mi>'
            r"</mrow></math> matrix.</p>"
        )
        self.assertIn(expected_body_2022, self.query_2022.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)
        self.assertEqual(QUERY_2022_TAGS, self.query_2022.tags)


class TestLoadAnswersText(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_TEXT[ANSWER_ID]

    def test_answer_body(self):
        self.assertIn(r"your answer written as  is correct too", self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadAnswersTextLaTeX(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_TEXT_LATEX[ANSWER_ID]

    def test_answer_body(self):
        expected_body = (
            r"your answer written as $ \frac{3}{2} \arctan\left(\frac{1+x}{2}\right)+\frac{1}{2} \log\left(5+2 "
            r"x+x^2\right)+C $ is correct too"
        )
        self.assertIn(expected_body, self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadAnswersTextTangentL(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_TEXT_TANGENTL[ANSWER_ID]

    def test_answer_body(self):
        expected_body = (
            r"your answer written as #(start)# #(f!,[n,o,u],-)# #(f!,[n,o,u])# #(f!,v!arctan,n,-)# "
            r"#(f!,v!arctan,n)# #(v!arctan,m!()1x1,n,n)# #(v!arctan,m!()1x1,n)# "
            r"#(m!()1x1,[n,w],nn)# #(m!()1x1,[n,w])# #(m!()1x1,+,n,nn)# #(m!()1x1,+,n)# "
            r"#(+,f!,n,nnn)# #(+,f!,n)# #(f!,[n,o,u],nnnn)# #(f!,[n,o,u])# #(f!,v!log,n,nnnn)# "
            r"#(f!,v!log,n)# #(v!log,m!()1x1,n,nnnnn)# #(v!log,m!()1x1,n)# #(m!()1x1,[n,w],6n)# "
            r"#(m!()1x1,[n,w])# #(m!()1x1,+,n,6n)# #(m!()1x1,+,n)# #(+,v!c,n,7n)# #(+,v!c,n)# "
            r"#(v!c,!0,8n)# #(v!c,!0)# #(m!()1x1,n!5,w,6n)# #(m!()1x1,n!5,w)# #(n!5,+,n,6n1w)# "
            r"#(n!5,+,n)# #(+,n!2,n,6n1w1n)# #(+,n!2,n)# #(n!2,v!x,n,6n1w2n)# #(n!2,v!x,n)# "
            r"#(v!x,+,n,6n1w3n)# #(v!x,+,n)# #(+,v!x,n,6n1w4n)# #(+,v!x,n)# #(v!x,n!2,a,6n1w5n)# "
            r"#(v!x,n!2,a)# #(n!2,!0,6n1w5n1a)# #(n!2,!0)# #{+,n,wnnnn,6n}# #{+,n,wnnnn}# "
            r"#{v!x,nn,6n1w3n}# #{v!x,nn}# #{n!2,nnna,6n1w2n}# #{n!2,nnna}# #{+,n,wn,6n}# "
            r"#{+,n,wn}# #{+,nnn,6n1w1n}# #{+,nnn}# #(f!,n!1,o,nnnn)# #(f!,n!1,o)# #(n!1,!0,nnnno)# "
            r"#(n!1,!0)# #(f!,n!2,u,nnnn)# #(f!,n!2,u)# #(n!2,!0,nnnnu)# #(n!2,!0)# "
            r"#{n!2,2n1w5n1a,u,nnnn}# #{n!2,2n1w5n1a,u}# #{n!2,nnwnn,u,nnnn}# #{n!2,nnwnn,u}# "
            r"#{+,nnnn,nnn}# #{+,nnnn}# #{+,3n1w4n,nnn}# #{+,3n1w4n}# #{+,nnnwn,nnn}# #{+,nnnwn}# "
            r"#(m!()1x1,f!,w,nn)# #(m!()1x1,f!,w)# #(f!,[o,u],nnw)# #(f!,[o,u])# #(f!,n!1,o,nnw)# "
            r"#(f!,n!1,o)# #(n!1,+,n,nnwo)# #(n!1,+,n)# #(+,v!x,n,nnwon)# #(+,v!x,n)# "
            r"#(v!x,!0,2n1w1o2n)# #(v!x,!0)# #{v!x,4n1w5n,wonn,nn}# #{v!x,4n1w5n,wonn}# "
            r"#{v!x,4n1w3n,wonn,nn}# #{v!x,4n1w3n,wonn}# #{+,nnnnn,won,nn}# #{+,nnnnn,won}# "
            r"#{+,4n1w4n,won,nn}# #{+,4n1w4n,won}# #{+,4n1w1n,won,nn}# #{+,4n1w1n,won}# "
            r"#{+,n,won,nn}# #{+,n,won}# #{n!1,nno,wo,nn}# #{n!1,nno,wo}# #(f!,n!2,u,nnw)# "
            r"#(f!,n!2,u)# #(n!2,!0,nnwu)# #(n!2,!0)# #{n!2,4n1w5n1a,wu,nn}# #{n!2,4n1w5n1a,wu}# "
            r"#{n!2,4n1w2n,wu,nn}# #{n!2,4n1w2n,wu}# #{n!2,nnu,wu,nn}# #{n!2,nnu,wu}# "
            r"#{f!,nn,w,nn}# #{f!,nn,w}# #{m!()1x1,nnnn,nn}# #{m!()1x1,nnnn}# #(f!,n!3,o,-)# "
            r"#(f!,n!3,o)# #(n!3,!0,o)# #(n!3,!0)# #(f!,n!2,u,-)# #(f!,n!2,u)# #(n!2,!0,u)# "
            r"#(n!2,!0)# #{n!2,6n1w5n1a,u,-}# #{n!2,6n1w5n1a,u}# #{n!2,6n1w2n,u,-}# "
            r"#{n!2,6n1w2n,u}# #{n!2,nnnnu,u,-}# #{n!2,nnnnu,u}# #{n!2,nnwu,u,-}# #{n!2,nnwu,u}# "
            r"#{f!,nnnn,-}# #{f!,nnnn}# #{f!,nnw,-}# #{f!,nnw}# #(end)# is correct too"
        )
        self.assertIn(expected_body, self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadAnswersTextPrefix(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_TEXT_PREFIX[ANSWER_ID]

    def test_answer_body(self):
        expected_body = (
            r"your answer written as U!plus U!times O!divide N!3 N!2 F!arctan O!divide U!plus N!1 V!𝑥 N!2 U!times "
            r"O!divide N!1 N!2 F!log U!plus N!5 U!times N!2 V!𝑥 O!SUP V!𝑥 N!2 V!𝐶 is correct too"
        )
        self.assertIn(expected_body, self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadAnswersTextXHTMLLaTeX(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_XHTML_LATEX[ANSWER_ID]

    def test_answer_body(self):
        expected_body = (
            r'your answer written as <span class="math-container" id="11236756"> \frac{3}{2} \arctan\left(\frac{1+x}{2}'
            r"\right)+\frac{1}{2} \log\left(5+2 x+x^2\right)+C </span> is correct too"
        )
        self.assertIn(expected_body, self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadAnswersTextXHTMLCMML(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_XHTML_CMML[ANSWER_ID]

    def test_answer_body(self):
        expected_body = (
            r'your answer written as <math xmlns="http://www.w3.org/1998/Math/MathML" encoding="MathML-Content"><apply>'
            r'<plus/><apply><times/><apply><divide/><cn type="integer">3</cn><cn type="integer">2</cn></apply><apply>'
            r'<arctan/><apply><divide/><apply><plus/><cn type="integer">1</cn><ci>𝑥</ci></apply><cn type="integer">2'
            r'</cn></apply></apply></apply><apply><times/><apply><divide/><cn type="integer">1</cn><cn type="integer">'
            r'2</cn></apply><apply><log/><apply><plus/><cn type="integer">5</cn><apply><times/><cn type="integer">2'
            r'</cn><ci>𝑥</ci></apply><apply><csymbol cd="ambiguous">superscript</csymbol><ci>𝑥</ci><cn type="integer">2'
            r"</cn></apply></apply></apply></apply><ci>𝐶</ci></apply></math> is correct too"
        )
        self.assertIn(expected_body, self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadAnswersTextXHTMLPMML(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_XHTML_PMML[ANSWER_ID]

    def test_answer_body(self):
        expected_body = (
            r'your answer written as <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="\frac{3}{2}\arctan'
            r'\left(\frac{1+x}{2}\right)+\frac{1}{2}\log\left(5+2x+x^{2}% \right)+C" class="ltx_Math" display="inline">'
            r"<mrow><mrow><mfrac><mn>3</mn><mn>2</mn></mfrac><mo>⁢</mo><mrow><mi>arctan</mi><mo>⁡</mo><mrow><mo>(</mo>"
            r"<mfrac><mrow><mn>1</mn><mo>+</mo><mi>x</mi></mrow><mn>2</mn></mfrac><mo>)</mo></mrow></mrow></mrow><mo>"
            r"+</mo><mrow><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>⁢</mo><mrow><mi>log</mi><mo>⁡</mo><mrow><mo>(</mo>"
            r"<mrow><mn>5</mn><mo>+</mo><mrow><mn>2</mn><mo>⁢</mo><mi>x</mi></mrow><mo>+</mo><msup><mi>x</mi><mn>2</mn>"
            r"</msup></mrow><mo>)</mo></mrow></mrow></mrow><mo>+</mo><mi>C</mi></mrow></math> is correct too"
        )
        self.assertIn(expected_body, self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadQuestionsText(unittest.TestCase):
    def setUp(self):
        self.question = QUESTIONS_TEXT[QUESTION_ID]

    def test_question_title(self):
        self.assertIn(QUESTION_TITLE, self.question.title)

    def test_question_body(self):
        self.assertIn(r"we cut off the set at any number .", self.question.body)

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, document_ids)


class TestLoadQuestionsTextLaTeX(unittest.TestCase):
    def setUp(self):
        self.question = QUESTIONS_TEXT_LATEX[QUESTION_ID]

    def test_question_title(self):
        self.assertIn(QUESTION_TITLE, self.question.title)

    def test_question_body(self):
        self.assertIn(r"we cut off the set at any number $n$.", self.question.body)

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, document_ids)


class TestLoadQuestionsTextTangentL(unittest.TestCase):
    def setUp(self):
        self.question = QUESTIONS_TEXT_TANGENTL[QUESTION_ID]

    def test_question_title(self):
        self.assertIn(QUESTION_TITLE, self.question.title)

    def test_question_body(self):
        self.assertIn(
            r"we cut off the set at any number #(start)# #(v!n,!0,-)# #(v!n,!0)# #(end)#.",
            self.question.body,
        )

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, document_ids)


class TestLoadQuestionsTextPrefix(unittest.TestCase):
    def setUp(self):
        self.question = QUESTIONS_TEXT_PREFIX[QUESTION_ID]

    def test_question_title(self):
        self.assertIn(QUESTION_TITLE, self.question.title)

    def test_question_body(self):
        self.assertIn(r"we cut off the set at any number V!𝑛.", self.question.body)

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, document_ids)


class TestLoadQuestionsXHTMLLaTeX(unittest.TestCase):
    def setUp(self):
        self.question = QUESTIONS_XHTML_LATEX[QUESTION_ID]

    def test_question_title(self):
        self.assertIn(QUESTION_TITLE, self.question.title)

    def test_question_body(self):
        self.assertIn(
            r'we cut off the set at any number <span class="math-container" id="6256370">n</span>',
            self.question.body,
        )

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, document_ids)


class TestLoadQuestionsXHTMLCMML(unittest.TestCase):
    def setUp(self):
        self.question = QUESTIONS_XHTML_CMML[QUESTION_ID]

    def test_question_title(self):
        self.assertIn(QUESTION_TITLE, self.question.title)

    def test_question_body(self):
        expected_body = (
            r'say we cut off the set at any number <math xmlns="http://www.w3.org/1998/Math/MathML" '
            r'encoding="MathML-Content"><ci>𝑛</ci></math>.'
        )
        self.assertIn(expected_body, self.question.body)

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, document_ids)


class TestLoadQuestionsXHTMLPMML(unittest.TestCase):
    def setUp(self):
        self.question = QUESTIONS_XHTML_PMML[QUESTION_ID]

    def test_question_title(self):
        self.assertIn(QUESTION_TITLE, self.question.title)

    def test_question_body(self):
        expected_body = (
            r'say we cut off the set at any number <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="n" '
            r'class="ltx_Math" display="inline"><mi>n</mi></math>.'
        )
        self.assertIn(expected_body, self.question.body)

    def test_question_tags(self):
        self.assertEqual(QUESTION_TAGS, self.question.tags)

    def test_question_upvotes(self):
        self.assertEqual(QUESTION_UPVOTES, self.question.upvotes)

    def test_question_views(self):
        self.assertEqual(QUESTION_VIEWS, self.question.views)

    def test_question_answers(self):
        document_ids = [answer.document_id for answer in self.question.answers]
        self.assertEqual(QUESTION_ANSWER_DOCUMENT_IDS, document_ids)


class TestLoadRelevanceJudgements(unittest.TestCase):
    def setUp(self):
        queries_2020 = load_queries("text", subset=None, year=2020)
        queries_2021 = load_queries("text", subset=None, year=2021)

        answers = ANSWERS_TEXT

        self.high_relevance_train_2020 = (
            queries_2020[HIGH_RELEVANCE_TRAIN_2020[0]],
            answers[HIGH_RELEVANCE_TRAIN_2020[1]],
        )
        self.medium_relevance_validation_2020 = (
            queries_2020[MEDIUM_RELEVANCE_VALIDATION_2020[0]],
            answers[MEDIUM_RELEVANCE_VALIDATION_2020[1]],
        )
        self.low_relevance_test_2020 = (
            queries_2020[LOW_RELEVANCE_TEST_2020[0]],
            answers[LOW_RELEVANCE_TEST_2020[1]],
        )
        self.no_relevance_2020 = (
            queries_2020[NO_RELEVANCE_2020[0]],
            answers[NO_RELEVANCE_2020[1]],
        )
        self.no_relevance_judgement_2020 = (
            queries_2020[NO_RELEVANCE_JUDGEMENT_2020[0]],
            answers[NO_RELEVANCE_JUDGEMENT_2020[1]],
        )

        self.high_relevance_2021 = (
            queries_2021[HIGH_RELEVANCE_2021[0]],
            answers[HIGH_RELEVANCE_2021[1]],
        )
        self.medium_relevance_2021 = (
            queries_2021[MEDIUM_RELEVANCE_2021[0]],
            answers[MEDIUM_RELEVANCE_2021[1]],
        )
        self.low_relevance_2021 = (
            queries_2021[LOW_RELEVANCE_2021[0]],
            answers[LOW_RELEVANCE_2021[1]],
        )
        self.no_relevance_2021 = (
            queries_2021[NO_RELEVANCE_2021[0]],
            answers[NO_RELEVANCE_2021[1]],
        )
        self.no_relevance_judgement_2021 = (
            queries_2021[NO_RELEVANCE_JUDGEMENT_2021[0]],
            answers[NO_RELEVANCE_JUDGEMENT_2021[1]],
        )

        self.judgements_2020 = load_judgements(
            queries_2020,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset=None,
        )
        self.judgements_train_2020 = load_judgements(
            queries_2020,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset="train",
        )
        self.judgements_validation_2020 = load_judgements(
            queries_2020,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset="validation",
        )
        self.judgements_test_2020 = load_judgements(
            queries_2020,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset="test",
        )

        self.judgements_2021 = load_judgements(
            queries_2021,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset=None,
            year=2021,
        )

    def test_judgements_high_relevance_train_2020(self):
        self.assertIn(self.high_relevance_train_2020, self.judgements_2020)
        self.assertIn(self.high_relevance_train_2020, self.judgements_train_2020)
        self.assertNotIn(
            self.high_relevance_train_2020, self.judgements_validation_2020
        )
        self.assertNotIn(self.high_relevance_train_2020, self.judgements_test_2020)

    def test_judgements_medium_relevance_validation_2020(self):
        self.assertIn(self.medium_relevance_validation_2020, self.judgements_2020)
        self.assertNotIn(
            self.medium_relevance_validation_2020, self.judgements_train_2020
        )
        self.assertIn(
            self.medium_relevance_validation_2020, self.judgements_validation_2020
        )
        self.assertNotIn(
            self.medium_relevance_validation_2020, self.judgements_test_2020
        )

    def test_judgements_low_relevance_test_2020(self):
        self.assertNotIn(self.low_relevance_test_2020, self.judgements_2020)
        self.assertNotIn(self.low_relevance_test_2020, self.judgements_train_2020)
        self.assertNotIn(self.low_relevance_test_2020, self.judgements_validation_2020)
        self.assertNotIn(self.low_relevance_test_2020, self.judgements_test_2020)

    def test_judgements_no_relevance_2020(self):
        self.assertNotIn(self.no_relevance_2020, self.judgements_2020)
        self.assertNotIn(self.no_relevance_2020, self.judgements_train_2020)
        self.assertNotIn(self.no_relevance_2020, self.judgements_validation_2020)
        self.assertNotIn(self.no_relevance_2020, self.judgements_test_2020)

    def test_judgements_no_relevance_judgement_2020(self):
        self.assertNotIn(self.no_relevance_judgement_2020, self.judgements_2020)
        self.assertNotIn(self.no_relevance_judgement_2020, self.judgements_train_2020)
        self.assertNotIn(
            self.no_relevance_judgement_2020, self.judgements_validation_2020
        )
        self.assertNotIn(self.no_relevance_judgement_2020, self.judgements_test_2020)

    def test_judgements_2021(self):
        self.assertIn(self.high_relevance_2021, self.judgements_2021)
        self.assertIn(self.medium_relevance_2021, self.judgements_2021)
        self.assertNotIn(self.low_relevance_2021, self.judgements_2021)
        self.assertNotIn(self.no_relevance_2021, self.judgements_2021)
        self.assertNotIn(self.no_relevance_judgement_2021, self.judgements_2021)
