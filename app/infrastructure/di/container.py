from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from app.infrastructure.di.app_provider import AppProvider
from app.infrastructure.di.http_provider import HTTPProvider
from app.infrastructure.di.use_case_provider import UseCaseProvider

container = make_async_container(
    AppProvider(), UseCaseProvider(), HTTPProvider(), FastapiProvider()
)
