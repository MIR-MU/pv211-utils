import unittest

from pv211_utils.arqmath.loader import load_queries, load_questions, load_answers, load_judgements


CACHE_DOWNLOAD = False

NUM_QUERIES_2020 = 77
NUM_QUERIES_2021 = 100

QUERY_2020_ID = 1
QUERY_2020_TAGS = ['functions']

QUERY_2021_ID = 201
QUERY_2021_TAGS = ['abstract-algebra', 'matrices', 'ring-theory']

QUESTION_ID = '614561'
QUESTION_TITLE = r'random thought: are some infinite sets larger than other'
QUESTION_UPVOTES = 3
QUESTION_VIEWS = 326
QUESTION_TAGS = ['infinity']
QUESTION_ANSWER_DOCUMENT_IDS = ['614568', '614563', '614564', '614565']

ANSWER_ID = '1199811'
ANSWER_UPVOTES = 1
ANSWER_IS_ACCEPTED = True

HIGH_RELEVANCE_TRAIN = (13, '563024')
MEDIUM_RELEVANCE_VALIDATION = (24, '1758902')
LOW_RELEVANCE_TEST = (16, '1002519')
NO_RELEVANCE = (40, '2106624')
NO_RELEVANCE_JUDGEMENT = (53, '377998')

ANSWER_IDS = set(
    QUESTION_ANSWER_DOCUMENT_IDS +
    [
        ANSWER_ID,
        HIGH_RELEVANCE_TRAIN[1],
        MEDIUM_RELEVANCE_VALIDATION[1],
        LOW_RELEVANCE_TEST[1],
        NO_RELEVANCE[1],
        NO_RELEVANCE_JUDGEMENT[1],
    ]
)
ANSWERS_TEXT = load_answers('text', cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS)
ANSWERS_TEXT_LATEX = load_answers('text+latex', cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS)
ANSWERS_TEXT_PREFIX = load_answers('text+prefix', cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS)
ANSWERS_XHTML_LATEX = load_answers('xhtml+latex', cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS)
ANSWERS_XHTML_CMML = load_answers('xhtml+cmml', cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS)
ANSWERS_XHTML_PMML = load_answers('xhtml+pmml', cache_download=CACHE_DOWNLOAD, filter_document_ids=ANSWER_IDS)


QUESTION_IDS = set([
    QUESTION_ID,
])
QUESTIONS_TEXT = load_questions('text', ANSWERS_TEXT, cache_download=CACHE_DOWNLOAD, filter_document_ids=QUESTION_IDS)
QUESTIONS_TEXT_LATEX = load_questions('text+latex', ANSWERS_TEXT_LATEX, cache_download=CACHE_DOWNLOAD,
                                      filter_document_ids=QUESTION_IDS)
QUESTIONS_TEXT_PREFIX = load_questions('text+prefix', ANSWERS_TEXT_PREFIX, cache_download=CACHE_DOWNLOAD,
                                       filter_document_ids=QUESTION_IDS)
QUESTIONS_XHTML_LATEX = load_questions('xhtml+latex', ANSWERS_XHTML_LATEX, cache_download=CACHE_DOWNLOAD,
                                       filter_document_ids=QUESTION_IDS)
QUESTIONS_XHTML_CMML = load_questions('xhtml+cmml', ANSWERS_XHTML_CMML, cache_download=CACHE_DOWNLOAD,
                                      filter_document_ids=QUESTION_IDS)
QUESTIONS_XHTML_PMML = load_questions('xhtml+pmml', ANSWERS_XHTML_PMML, cache_download=CACHE_DOWNLOAD,
                                      filter_document_ids=QUESTION_IDS)


class TestLoadQueriesText(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries('text', subset=None, year=2020)
        self.queries_2021 = load_queries('text', subset=None, year=2021)
        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))

    def test_query_title(self):
        self.assertIn(r'Finding value of  such that', self.query_2020.title)
        self.assertEqual(r'Matrix over division ring having one sided inverse is invertible',
                         self.query_2021.title)

    def test_query_body(self):
        self.assertIn(r'If  then find the value of  ', self.query_2020.body)
        self.assertIn(r'If an  matrix over a division ring', self.query_2021.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)


class TestLoadQueriesLaTeX(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries('text+latex', subset=None, year=2020)
        self.queries_2021 = load_queries('text+latex', subset=None, year=2021)
        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))

    def test_query_title(self):
        self.assertIn(r'Finding value of $c$ such that', self.query_2020.title)
        self.assertEqual(r'Matrix over division ring having one sided inverse is invertible',
                         self.query_2021.title)

    def test_query_body(self):
        self.assertIn(r'If $f(x)= \frac{x^2 + x + c}{x^2 + 2x + c}$ then find the value of $c$',
                      self.query_2020.body)
        self.assertIn(r'If an $n\times n$ matrix over a division ring', self.query_2021.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)


class TestLoadQueriesPrefix(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries('text+prefix', subset=None, year=2020)
        self.queries_2021 = load_queries('text+prefix', subset=None, year=2021)
        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))

    def test_query_title(self):
        self.assertIn(r'Finding value of V!𝑐 such that', self.query_2020.title)
        self.assertEqual(r'Matrix over division ring having one sided inverse is invertible',
                         self.query_2021.title)

    def test_query_body(self):
        expected_body_2020 = (
            r'If U!eq U!times V!𝑓 V!𝑥 O!divide U!plus O!SUP V!𝑥 N!2 V!𝑥 V!𝑐 U!plus O!SUP V!𝑥 N!2 U!times N!2 V!𝑥 '
            r'V!𝑐 then find the value of V!𝑐'
        )
        self.assertIn(expected_body_2020, self.query_2020.body)
        self.assertIn(r'If an U!times V!𝑛 V!𝑛 matrix over a division ring', self.query_2021.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)


class TestLoadQueriesXHTMLLaTeX(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries('xhtml+latex', subset=None, year=2020)
        self.queries_2021 = load_queries('xhtml+latex', subset=None, year=2021)
        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))

    def test_query_title(self):
        self.assertIn(r'Finding value of <span class="math-container" id="q_1">$c$</span> such that',
                      self.query_2020.title)
        self.assertEqual(r'Matrix over division ring having one sided inverse is invertible',
                         self.query_2021.title)

    def test_query_body(self):
        expected_body_2020 = (
            r'<p>If <span class="math-container" id="q_4">$$f(x)= \frac{x^2 + x + c}{x^2 + 2x + c}$$</span> then '
            r'find the value of <span class="math-container" id="q_5">$c$</span>'
        )
        self.assertIn(expected_body_2020, self.query_2020.body)

        expected_body_2021 = (
            r'<p><em>If an <span class="math-container" id="q_1">$n\times n$</span> matrix over '
            r'a division ring'
        )
        self.assertIn(expected_body_2021, self.query_2021.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)


class TestLoadQueriesXHTMLCMML(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries('xhtml+cmml', subset=None, year=2020)
        self.queries_2021 = load_queries('xhtml+cmml', subset=None, year=2021)
        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))

    def test_query_title(self):
        expected_title_2020 = (
            r'<p>Finding value of <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="c" display="block"> '
            r'<ci>𝑐</ci> </math> such that'
        )
        self.assertIn(expected_title_2020, self.query_2020.title)

        self.assertEqual(r'<p>Matrix over division ring having one sided inverse is invertible</p>',
                         self.query_2021.title)

    def test_query_body(self):
        expected_body_2020 = (
            r'If <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="f(x)=\frac{x^{2}+x+c}{x^{2}+2x+c}" '
            r'display="block"> <apply> <eq/> <apply> <times/> <ci>𝑓</ci> <ci>𝑥</ci> </apply> <apply> <divide/> <apply> '
            r'<plus/> <apply> <csymbol cd="ambiguous">superscript</csymbol> <ci>𝑥</ci> <cn type="integer">2</cn> '
            r'</apply> <ci>𝑥</ci> <ci>𝑐</ci> </apply> <apply> <plus/> <apply> <csymbol cd="ambiguous">superscript'
            r'</csymbol> <ci>𝑥</ci> <cn type="integer">2</cn> </apply> <apply> <times/> <cn type="integer">2</cn> '
            r'<ci>𝑥</ci> </apply> <ci>𝑐</ci> </apply> </apply> </apply> </math> then find the value of '
            r'<math xmlns="http://www.w3.org/1998/Math/MathML" alttext="c" display="block"> <ci>𝑐</ci> </math>'
        )
        self.assertIn(expected_body_2020, self.query_2020.body)

        expected_body_2021 = (
            r'<p><em>If an <math xmlns="http://www.w3.org/1998/Math/MathML" encoding="MathML-Content">'
            r'<apply><times/><ci>𝑛</ci><ci>𝑛</ci></apply></math> matrix over a division ring'
        )
        self.assertIn(expected_body_2021, self.query_2021.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)


class TestLoadQueriesXHTMLPMML(unittest.TestCase):
    def setUp(self):
        self.queries_2020 = load_queries('xhtml+pmml', subset=None, year=2020)
        self.queries_2021 = load_queries('xhtml+pmml', subset=None, year=2021)
        self.query_2020 = self.queries_2020[QUERY_2020_ID]
        self.query_2021 = self.queries_2021[QUERY_2021_ID]

    def test_number_of_queries(self):
        self.assertEqual(NUM_QUERIES_2020, len(self.queries_2020))
        self.assertEqual(NUM_QUERIES_2021, len(self.queries_2021))

    def test_query_title(self):
        expected_title_2020 = (
            r'<p>Finding value of <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="c" display="block"> '
            r'<mi>c</mi> </math> such that'
        )
        self.assertIn(expected_title_2020, self.query_2020.title)

        self.assertEqual(r'<p>Matrix over division ring having one sided inverse is invertible</p>',
                         self.query_2021.title)

    def test_query_body(self):
        expected_body_2020 = (
            r'<math xmlns="http://www.w3.org/1998/Math/MathML" alttext="f(x)=\frac{x^{2}+x+c}{x^{2}+2x+c}" '
            r'display="block"> <mrow> <mrow> <mi>f</mi> <mo>⁢</mo> <mrow> <mo stretchy="false">(</mo> <mi>x</mi> '
            r'<mo stretchy="false">)</mo> </mrow> </mrow> <mo>=</mo> <mfrac> <mrow> <msup> <mi>x</mi> <mn>2</mn> '
            r'</msup> <mo>+</mo> <mi>x</mi> <mo>+</mo> <mi>c</mi> </mrow> <mrow> <msup> <mi>x</mi> <mn>2</mn> </msup> '
            r'<mo>+</mo> <mrow> <mn>2</mn> <mo>⁢</mo> <mi>x</mi> </mrow> <mo>+</mo> <mi>c</mi> </mrow> </mfrac> '
            r'</mrow> </math> then find the value of <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="c" '
            r'display="block"> <mi>c</mi> </math>'
        )
        self.assertIn(expected_body_2020, self.query_2020.body)

        expected_body_2021 = (
            r'<p><em>If an <math xmlns="http://www.w3.org/1998/Math/MathML" alttext="n\times n" '
            r'class="ltx_Math" display="inline"><mrow><mi>n</mi><mo>×</mo><mi>n</mi></mrow></math> '
            r'matrix over a division ring'
        )
        self.assertIn(expected_body_2021, self.query_2021.body)

    def test_query_tags(self):
        self.assertEqual(QUERY_2020_TAGS, self.query_2020.tags)
        self.assertEqual(QUERY_2021_TAGS, self.query_2021.tags)


class TestLoadAnswersText(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_TEXT[ANSWER_ID]

    def test_answer_body(self):
        self.assertIn(r'your answer written as  is correct too', self.answer.body)

    def test_answer_upvotes(self):
        self.assertEqual(ANSWER_UPVOTES, self.answer.upvotes)

    def test_answer_is_accepted(self):
        self.assertEqual(ANSWER_IS_ACCEPTED, self.answer.is_accepted)


class TestLoadAnswersTextLaTeX(unittest.TestCase):
    def setUp(self):
        self.answer = ANSWERS_TEXT_LATEX[ANSWER_ID]

    def test_answer_body(self):
        expected_body = (
            r'your answer written as $ \frac{3}{2} \arctan\left(\frac{1+x}{2}\right)+\frac{1}{2} \log\left(5+2 '
            r'x+x^2\right)+C $ is correct too'
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
            r'your answer written as U!plus U!times O!divide N!3 N!2 F!arctan O!divide U!plus N!1 V!𝑥 N!2 U!times '
            r'O!divide N!1 N!2 F!log U!plus N!5 U!times N!2 V!𝑥 O!SUP V!𝑥 N!2 V!𝐶 is correct too'
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
            r'\right)+\frac{1}{2} \log\left(5+2 x+x^2\right)+C </span> is correct too'
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
            r'</cn></apply></apply></apply></apply><ci>𝐶</ci></apply></math> is correct too'
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
            r'<mrow><mrow><mfrac><mn>3</mn><mn>2</mn></mfrac><mo>⁢</mo><mrow><mi>arctan</mi><mo>⁡</mo><mrow><mo>(</mo>'
            r'<mfrac><mrow><mn>1</mn><mo>+</mo><mi>x</mi></mrow><mn>2</mn></mfrac><mo>)</mo></mrow></mrow></mrow><mo>'
            r'+</mo><mrow><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>⁢</mo><mrow><mi>log</mi><mo>⁡</mo><mrow><mo>(</mo>'
            r'<mrow><mn>5</mn><mo>+</mo><mrow><mn>2</mn><mo>⁢</mo><mi>x</mi></mrow><mo>+</mo><msup><mi>x</mi><mn>2</mn>'
            r'</msup></mrow><mo>)</mo></mrow></mrow></mrow><mo>+</mo><mi>C</mi></mrow></math> is correct too'
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
        self.assertIn(r'we cut off the set at any number .', self.question.body)

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
        self.assertIn(r'we cut off the set at any number $n$.', self.question.body)

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
        self.assertIn(r'we cut off the set at any number V!𝑛.', self.question.body)

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
        self.assertIn(r'we cut off the set at any number <span class="math-container" id="6256370">n</span>',
                      self.question.body)

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
        queries = load_queries('text', subset=None)
        answers = ANSWERS_TEXT
        self.high_relevance_train = (
            queries[HIGH_RELEVANCE_TRAIN[0]],
            answers[HIGH_RELEVANCE_TRAIN[1]],
        )
        self.medium_relevance_validation = (
            queries[MEDIUM_RELEVANCE_VALIDATION[0]],
            answers[MEDIUM_RELEVANCE_VALIDATION[1]],
        )
        self.low_relevance_test = (
            queries[LOW_RELEVANCE_TEST[0]],
            answers[LOW_RELEVANCE_TEST[1]],
        )
        self.no_relevance = (queries[NO_RELEVANCE[0]], answers[NO_RELEVANCE[1]])
        self.no_relevance_judgement = (queries[NO_RELEVANCE_JUDGEMENT[0]], answers[NO_RELEVANCE_JUDGEMENT[1]])

        self.judgements = load_judgements(
            queries,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset=None,
        )
        self.judgements_train = load_judgements(
            queries,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset='train',
        )
        self.judgements_validation = load_judgements(
            queries,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset='validation',
        )
        self.judgements_test = load_judgements(
            queries,
            answers,
            filter_document_ids=ANSWER_IDS,
            subset='test',
        )

    def test_judgements_high_relevance_train(self):
        self.assertIn(self.high_relevance_train, self.judgements)
        self.assertIn(self.high_relevance_train, self.judgements_train)
        self.assertNotIn(self.high_relevance_train, self.judgements_validation)
        self.assertNotIn(self.high_relevance_train, self.judgements_test)

    def test_judgements_medium_relevance_validation(self):
        self.assertIn(self.medium_relevance_validation, self.judgements)
        self.assertNotIn(self.medium_relevance_validation, self.judgements_train)
        self.assertIn(self.medium_relevance_validation, self.judgements_validation)
        self.assertNotIn(self.medium_relevance_validation, self.judgements_test)

    def test_judgements_low_relevance_test(self):
        self.assertNotIn(self.low_relevance_test, self.judgements)
        self.assertNotIn(self.low_relevance_test, self.judgements_train)
        self.assertNotIn(self.low_relevance_test, self.judgements_validation)
        self.assertNotIn(self.low_relevance_test, self.judgements_test)

    def test_judgements_no_relevance(self):
        self.assertNotIn(self.no_relevance, self.judgements)
        self.assertNotIn(self.no_relevance, self.judgements_train)
        self.assertNotIn(self.no_relevance, self.judgements_validation)
        self.assertNotIn(self.no_relevance, self.judgements_test)

    def test_judgements_no_relevance_judgement(self):
        self.assertNotIn(self.no_relevance_judgement, self.judgements)
        self.assertNotIn(self.no_relevance_judgement, self.judgements_train)
        self.assertNotIn(self.no_relevance_judgement, self.judgements_validation)
        self.assertNotIn(self.no_relevance_judgement, self.judgements_test)
