import motorengine
from datetime import datetime
from mongomock import gridfs

gridfs.enable_gridfs_integration()
motorengine.connect(
    "graphene-motorengine-test", host="mongomock://localhost", alias="default"
)
# motorengine.connect('graphene-motorengine-test', host='mongodb://localhost/graphene-motorengine-dev')


class Publisher(motorengine.Document):

    meta = {"collection": "test_publisher"}
    name = motorengine.StringField()

    @property
    def legal_name(self):
        return self.name + " Inc."

    def bad_field(self):
        return None


class Editor(motorengine.Document):
    """
    An Editor of a publication.
    """

    meta = {"collection": "test_editor"}
    id = motorengine.StringField(primary_key=True)
    first_name = motorengine.StringField(
        required=True, help_text="Editor's first name.", db_field="fname"
    )
    last_name = motorengine.StringField(required=True, help_text="Editor's last name.")
    metadata = motorengine.MapField(
        field=motorengine.StringField(), help_text="Arbitrary metadata."
    )
    company = motorengine.LazyReferenceField(Publisher)
    avatar = motorengine.FileField()
    seq = motorengine.SequenceField()


class Article(motorengine.Document):

    meta = {"collection": "test_article"}
    headline = motorengine.StringField(required=True, help_text="The article headline.")
    pub_date = motorengine.DateTimeField(
        default=datetime.now,
        verbose_name="publication date",
        help_text="The date of first press.",
    )
    editor = motorengine.ReferenceField(Editor)
    reporter = motorengine.ReferenceField("Reporter")
    # Will not convert these fields cause no choices
    # generic_reference = motorengine.GenericReferenceField()
    # generic_embedded_document = motorengine.GenericEmbeddedDocumentField()


class EmbeddedArticle(motorengine.EmbeddedDocument):

    meta = {"collection": "test_embedded_article"}
    headline = motorengine.StringField(required=True)
    pub_date = motorengine.DateTimeField(default=datetime.now)
    editor = motorengine.ReferenceField(Editor)
    reporter = motorengine.ReferenceField("Reporter")


class EmbeddedFoo(motorengine.EmbeddedDocument):
    meta = {"collection": "test_embedded_foo"}
    bar = motorengine.StringField()


class Reporter(motorengine.Document):

    meta = {"collection": "test_reporter"}
    id = motorengine.StringField(primary_key=True)
    first_name = motorengine.StringField(required=True)
    last_name = motorengine.StringField(required=True)
    email = motorengine.EmailField()
    awards = motorengine.ListField(motorengine.StringField())
    articles = motorengine.ListField(motorengine.ReferenceField(Article))
    embedded_articles = motorengine.ListField(
        motorengine.EmbeddedDocumentField(EmbeddedArticle)
    )
    embedded_list_articles = motorengine.EmbeddedDocumentListField(EmbeddedArticle)
    generic_reference = motorengine.GenericReferenceField(choices=[Article, Editor])
    generic_embedded_document = motorengine.GenericEmbeddedDocumentField(
        choices=[EmbeddedArticle, EmbeddedFoo]
    )
    generic_references = motorengine.ListField(
        motorengine.GenericReferenceField(choices=[Article, Editor])
    )


class Player(motorengine.Document):

    meta = {"collection": "test_player"}
    first_name = motorengine.StringField(required=True)
    last_name = motorengine.StringField(required=True)
    opponent = motorengine.ReferenceField("Player")
    players = motorengine.ListField(motorengine.ReferenceField("Player"))
    articles = motorengine.ListField(motorengine.ReferenceField("Article"))
    embedded_list_articles = motorengine.EmbeddedDocumentListField(EmbeddedArticle)


class Parent(motorengine.Document):

    meta = {"collection": "test_parent", "allow_inheritance": True}
    bar = motorengine.StringField()
    loc = motorengine.MultiPolygonField()


class CellTower(motorengine.Document):

    meta = {"collection": "test_cell_tower"}
    code = motorengine.StringField()
    base = motorengine.PolygonField()
    coverage_area = motorengine.MultiPolygonField()


class Child(Parent):

    meta = {"collection": "test_child"}
    baz = motorengine.StringField()
    loc = motorengine.PointField()


class ProfessorMetadata(motorengine.EmbeddedDocument):

    meta = {"collection": "test_professor_metadata"}
    id = motorengine.StringField(primary_key=False)
    first_name = motorengine.StringField()
    last_name = motorengine.StringField()
    departments = motorengine.ListField(motorengine.StringField())


class ProfessorVector(motorengine.Document):

    meta = {"collection": "test_professor_vector"}
    vec = motorengine.ListField(motorengine.FloatField())
    metadata = motorengine.EmbeddedDocumentField(ProfessorMetadata)


class ParentWithRelationship(motorengine.Document):

    meta = {"collection": "test_parent_reference"}
    before_child = motorengine.ListField(
        motorengine.ReferenceField("ChildRegisteredBefore")
    )
    after_child = motorengine.ListField(
        motorengine.ReferenceField("ChildRegisteredAfter")
    )
    name = motorengine.StringField()


class ChildRegisteredBefore(motorengine.Document):

    meta = {"collection": "test_child_before_reference"}
    parent = motorengine.ReferenceField(ParentWithRelationship)
    name = motorengine.StringField()


class ChildRegisteredAfter(motorengine.Document):

    meta = {"collection": "test_child_after_reference"}
    parent = motorengine.ReferenceField(ParentWithRelationship)
    name = motorengine.StringField()


class ErroneousModel(motorengine.Document):
    meta = {"collection": "test_colliding_objects_model"}

    objects = motorengine.ListField(motorengine.StringField())


class Bar(motorengine.EmbeddedDocument):
    some_list_field = motorengine.ListField(motorengine.StringField(), required=True)


class Foo(motorengine.Document):
    bars = motorengine.EmbeddedDocumentListField(Bar)
