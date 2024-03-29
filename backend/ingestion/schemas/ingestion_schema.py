# -*- coding: utf-8 -*-
from enum import Enum

from langchain.document_loaders.base import BaseLoader
from langchain_community.document_loaders import (
    PDFMinerLoader,
    PDFMinerPDFasHTMLLoader,
    PyMuPDFLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPDFLoader,
)


class PDFParserEnum(Enum):
    PyMuPDF = "PyMuPDF"
    PDFMiner_HTML = "PDFMiner_HTML"
    PDFMiner = "PDFMiner"
    PyPDF = "PyPDF"
    Unstructured = "Unstructured"
    PyPDF2Custom = "PyPDF2Custom"


class MDParserEnum(Enum):
    MDUnstructured = "MDUnstructured"


LOADER_DICT: dict[str, type[BaseLoader]] = {
    PDFParserEnum.PyPDF.name: PyPDFLoader,
    PDFParserEnum.PyMuPDF.name: PyMuPDFLoader,
    PDFParserEnum.PDFMiner.name: PDFMinerLoader,
    PDFParserEnum.PDFMiner_HTML.name: PDFMinerPDFasHTMLLoader,
    PDFParserEnum.Unstructured.name: UnstructuredPDFLoader,
    MDParserEnum.MDUnstructured.name: UnstructuredMarkdownLoader,
}
