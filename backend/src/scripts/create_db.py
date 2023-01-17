import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from src.container import container
from src.data import mapper_registry
from src.data.uow import UnitOfWork


async def main() -> None:
    uow: UnitOfWork = container.uow()
    async with uow:
        async with uow.engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.create_all)
        await uow.commit()


if __name__ == "__main__":
    asyncio.run(main())
