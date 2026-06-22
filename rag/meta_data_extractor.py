import langextract as lx
import textwrap
from dotenv import load_dotenv

load_dotenv()

PROMPT = textwrap.dedent("""\
Extract entities and relationships from this programming document.
The document may be written in any programming language (e.g. Python,
JavaScript/TypeScript, Java, C#, Go, Rust, C/C++, Ruby, PHP, Kotlin, Swift, etc.).
Identify entities and relationships using the language's own syntax and
conventions, but map them to the generic categories below.

Entities:
- Classes (or structs/interfaces/traits where the language has no "class")
- Functions
- Methods
- Modules (or packages/namespaces/files, depending on language)
- Packages
- APIs (endpoints, routes, RPC calls, public interfaces)
- Database Tables
- Models (data classes, DTOs, schemas, entities)
- Design Patterns
- Technical Concepts

Relationships:
- Class USES Class
- Function CALLS Function
- Class INHERITS Class (or IMPLEMENTS Interface)
- Module IMPORTS Module
- API USES Model
- Model MAPS_TO Table
- Function RETURNS Type
- Function ACCEPTS Parameter

Use exact names from the document, written exactly as they appear in that
language's syntax (e.g. respect each language's naming conventions such as
camelCase, snake_case, or PascalCase rather than normalizing them).

Return structured metadata that can be used to build:
- Knowledge Graphs
- Vector Database Metadata
- Code Search Systems
- Repository Documentation
""")


EXAMPLES = [
    # Python example
    lx.data.ExampleData(
        text="""
import requests

class GitHubClient:
    def get_repo(self, repo_name):
        return requests.get(f"/repos/{repo_name}")
""",
        extractions=[
            lx.data.Extraction(
                extraction_class="module",
                extraction_text="requests",
                attributes={
                    "language": "python",
                    "type": "imported_package"
                }
            ),
            lx.data.Extraction(
                extraction_class="class",
                extraction_text="GitHubClient",
                attributes={
                    "language": "python",
                    "role": "client_class"
                }
            ),
            lx.data.Extraction(
                extraction_class="method",
                extraction_text="get_repo",
                attributes={
                    "language": "python",
                    "parent_class": "GitHubClient"
                }
            ),
            lx.data.Extraction(
                extraction_class="api",
                extraction_text="/repos/{repo_name}",
                attributes={
                    "language": "python",
                    "type": "repository_endpoint"
                }
            )
        ]
    ),

    # Python example with inheritance and a model
    lx.data.ExampleData(
        text="""
class UserService(BaseService):

    def create_user(self, username: str) -> User:
        return User(username=username)
""",
        extractions=[
            lx.data.Extraction(
                extraction_class="class",
                extraction_text="UserService",
                attributes={
                    "language": "python",
                    "role": "service_class"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="BaseService",
                attributes={
                    "language": "python",
                    "type": "inherits",
                    "from_class": "UserService",
                    "to_class": "BaseService"
                }
            ),
            lx.data.Extraction(
                extraction_class="function",
                extraction_text="create_user",
                attributes={
                    "language": "python",
                    "returns": "User"
                }
            ),
            lx.data.Extraction(
                extraction_class="parameter",
                extraction_text="username",
                attributes={
                    "language": "python",
                    "datatype": "str"
                }
            ),
            lx.data.Extraction(
                extraction_class="model",
                extraction_text="User",
                attributes={
                    "language": "python",
                    "role": "domain_model"
                }
            )
        ]
    ),

    # Python ORM-style model mapped to a table
    lx.data.ExampleData(
        text="""
from sqlmodel import SQLModel, Field

class Customer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
""",
        extractions=[
            lx.data.Extraction(
                extraction_class="module",
                extraction_text="sqlmodel",
                attributes={
                    "language": "python",
                    "type": "library"
                }
            ),
            lx.data.Extraction(
                extraction_class="model",
                extraction_text="Customer",
                attributes={
                    "language": "python",
                    "table": "true"
                }
            ),
            lx.data.Extraction(
                extraction_class="field",
                extraction_text="id",
                attributes={
                    "language": "python",
                    "primary_key": "true"
                }
            ),
            lx.data.Extraction(
                extraction_class="field",
                extraction_text="name",
                attributes={
                    "language": "python",
                    "datatype": "str"
                }
            )
        ]
    ),

    # JavaScript/TypeScript example
    lx.data.ExampleData(
        text="""
import axios from 'axios';

class OrderService extends BaseService {
    async getOrder(orderId: string): Promise<Order> {
        return axios.get(`/api/orders/${orderId}`);
    }
}
""",
        extractions=[
            lx.data.Extraction(
                extraction_class="module",
                extraction_text="axios",
                attributes={
                    "language": "typescript",
                    "type": "imported_package"
                }
            ),
            lx.data.Extraction(
                extraction_class="class",
                extraction_text="OrderService",
                attributes={
                    "language": "typescript",
                    "role": "service_class"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="OrderService -> BaseService",
                attributes={
                    "language": "typescript",
                    "type": "inherits"
                }
            ),
            lx.data.Extraction(
                extraction_class="method",
                extraction_text="getOrder",
                attributes={
                    "language": "typescript",
                    "parent_class": "OrderService",
                    "returns": "Promise<Order>"
                }
            ),
            lx.data.Extraction(
                extraction_class="parameter",
                extraction_text="orderId",
                attributes={
                    "language": "typescript",
                    "datatype": "string"
                }
            ),
            lx.data.Extraction(
                extraction_class="api",
                extraction_text="/api/orders/${orderId}",
                attributes={
                    "language": "typescript",
                    "type": "order_endpoint"
                }
            ),
            lx.data.Extraction(
                extraction_class="model",
                extraction_text="Order",
                attributes={
                    "language": "typescript",
                    "role": "domain_model"
                }
            )
        ]
    ),

    # Java example
    lx.data.ExampleData(
        text="""
package com.example.billing;

import java.util.List;

public class InvoiceRepository implements Repository<Invoice> {

    public List<Invoice> findByCustomerId(String customerId) {
        return jdbcTemplate.query("SELECT * FROM invoices WHERE customer_id = ?", customerId);
    }
}
""",
        extractions=[
            lx.data.Extraction(
                extraction_class="package",
                extraction_text="com.example.billing",
                attributes={
                    "language": "java",
                    "type": "namespace"
                }
            ),
            lx.data.Extraction(
                extraction_class="module",
                extraction_text="java.util.List",
                attributes={
                    "language": "java",
                    "type": "imported_class"
                }
            ),
            lx.data.Extraction(
                extraction_class="class",
                extraction_text="InvoiceRepository",
                attributes={
                    "language": "java",
                    "role": "repository_class"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="InvoiceRepository -> Repository<Invoice>",
                attributes={
                    "language": "java",
                    "type": "implements"
                }
            ),
            lx.data.Extraction(
                extraction_class="method",
                extraction_text="findByCustomerId",
                attributes={
                    "language": "java",
                    "parent_class": "InvoiceRepository",
                    "returns": "List<Invoice>"
                }
            ),
            lx.data.Extraction(
                extraction_class="parameter",
                extraction_text="customerId",
                attributes={
                    "language": "java",
                    "datatype": "String"
                }
            ),
            lx.data.Extraction(
                extraction_class="table",
                extraction_text="invoices",
                attributes={
                    "language": "java",
                    "type": "database_table"
                }
            ),
            lx.data.Extraction(
                extraction_class="model",
                extraction_text="Invoice",
                attributes={
                    "language": "java",
                    "role": "domain_model"
                }
            )
        ]
    ),

    # Go example
    lx.data.ExampleData(
        text="""
package handlers

import "net/http"

type ProductHandler struct {
    Service ProductService
}

func (h *ProductHandler) GetProduct(w http.ResponseWriter, r *http.Request) {
    h.Service.FindByID(r.URL.Query().Get("id"))
}
""",
        extractions=[
            lx.data.Extraction(
                extraction_class="package",
                extraction_text="handlers",
                attributes={
                    "language": "go",
                    "type": "namespace"
                }
            ),
            lx.data.Extraction(
                extraction_class="module",
                extraction_text="net/http",
                attributes={
                    "language": "go",
                    "type": "imported_package"
                }
            ),
            lx.data.Extraction(
                extraction_class="class",
                extraction_text="ProductHandler",
                attributes={
                    "language": "go",
                    "role": "struct_as_class"
                }
            ),
            lx.data.Extraction(
                extraction_class="function",
                extraction_text="GetProduct",
                attributes={
                    "language": "go",
                    "parent_class": "ProductHandler",
                    "role": "http_handler"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="ProductHandler -> ProductService",
                attributes={
                    "language": "go",
                    "type": "uses"
                }
            ),
            lx.data.Extraction(
                extraction_class="function",
                extraction_text="FindByID",
                attributes={
                    "language": "go",
                    "parent_class": "ProductService"
                }
            )
        ]
    )
]


def build_doc_metadata(extractions):
    """Group grounded extractions by class for document-level summary use
    (e.g. logging, debugging, or a separate doc-level metadata store)."""
    meta = {}
    for e in extractions:
        meta.setdefault(e.extraction_class, []).append({
            "text": e.extraction_text,
            **(e.attributes or {})
        })
    return meta


def extract_meta_data(document_text: str):
    result = lx.extract(
        text_or_documents=document_text,
        prompt_description=PROMPT,
        examples=EXAMPLES,
        model_id="gemini-2.5-flash",
        # model_id="llama3",  # Automatically selects Ollama provider
        # model_url="http://localhost:11434",
        extraction_passes=1,     # better recall for longer docs
        max_workers=1,
        # timeout=600
    )

    # Keep only extractions LangExtract could ground in the source text
    grounded = [e for e in result.extractions if e.char_interval]

    # Return the grounded extraction objects themselves (not just the
    # grouped summary) so callers can match entities to individual chunks.
    return grounded


def tag_chunks_with_entities(chunks, grounded_extractions, max_per_field=20):
    """Attach relevant LangExtract entities to each LangChain Document chunk's
    metadata, based on substring presence of the entity text in the chunk.

    This is a presence/substring match rather than a char_interval match,
    because char_interval is relative to the full extraction-time document
    text, while `chunks` here are produced by a separate loader + splitter
    pass (e.g. PyPDFLoader -> RecursiveCharacterTextSplitter) whose page/chunk
    boundaries don't share the same offsets. Substring matching is more
    robust across that boundary, at the cost of being approximate (e.g. it
    can't distinguish two same-named entities defined in different scopes).

    Args:
        chunks: list of langchain_core.documents.Document
        grounded_extractions: list of lx.data.Extraction (from extract_meta_data)
        max_per_field: cap on how many entity strings to store per field,
            to keep Qdrant payloads small for chunks that happen to match a lot

    Returns:
        The same list of chunks, mutated in place, with metadata populated.
    """
    # Pre-bucket extraction texts by class once, so we're not re-grouping
    # per chunk.
    by_class = {}
    for e in grounded_extractions:
        text = e.extraction_text.strip()
        if not text:
            continue
        by_class.setdefault(e.extraction_class, set()).add(text)

    for chunk in chunks:
        chunk_text = chunk.page_content
        for entity_class, entity_texts in by_class.items():
            matches = [t for t in entity_texts if t in chunk_text]
            if matches:
                # e.g. chunk.metadata["entities_class"] = [...]
                field_name = f"entities_{entity_class}"
                chunk.metadata[field_name] = sorted(matches)[:max_per_field]

    return chunks