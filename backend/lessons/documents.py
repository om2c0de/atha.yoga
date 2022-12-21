from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, token_filter

from lessons.models import Course

ru_analyzer = analyzer(
    "ru",
    tokenizer="standard",
    filter=[
        "lowercase",
        token_filter(
            "ru_stopwords",
            type="stop",
            stopwords="а,без,более,бы,был,была,были,было,быть,в,вам,вас,весь,во,вот,все,всего,всех,вы,где,да,"
            "даже,для,до,его,ее,если,есть,еще,же,за,здесь,и,из,или,им,их,к,как,ко,когда,кто,ли,либо,"
            "мне,может,мы,на,надо,наш,не,него,нее,нет,ни,них,но,ну,о,об,однако,он,она,они,оно,от,"
            "очень,по,под,при,с,со,так,также,такой,там,те,тем,то,того,тоже,той,только,том,ты,у,уже,"
            "хотя,чего,чей,чем,что,чтобы,чье,чья,эта,эти,это,я,a,an,and,are,as,at,be,but,by,for,"
            "if,in,into,is,it,no,not,of,on,or,such,that,the,their,then,there,these,they,this,to,was,"
            "will,with",
        ),
        token_filter("ru_stemming", type="snowball", language="Russian"),
        token_filter("ru", type="hunspell", locale="ru_RU"),
    ],
)


@registry.register_document
class CourseDocument(Document):
    name = fields.TextField(analyzer=ru_analyzer)
    description = fields.TextField(analyzer=ru_analyzer)

    class Index:
        name = "courses"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Course
