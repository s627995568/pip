from pip._vendor.packaging.specifiers import SpecifierSet
from pip._vendor.resolvelib.providers import AbstractProvider

from pip._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from typing import Any, Dict, Optional, Sequence, Tuple, Union

    from pip._internal.req.req_install import InstallRequirement

    from .base import Requirement, Candidate
    from .factory import Factory


class PipProvider(AbstractProvider):
    def __init__(
        self,
        factory,  # type: Factory
        constraints,  # type: Dict[str, SpecifierSet]
        ignore_dependencies,  # type: bool
    ):
        # type: (...) -> None
        self._factory = factory
        self._constraints = constraints
        self._ignore_dependencies = ignore_dependencies

    def get_install_requirement(self, c):
        # type: (Candidate) -> Optional[InstallRequirement]
        return c.get_install_requirement()

    def identify(self, dependency):
        # type: (Union[Requirement, Candidate]) -> str
        return dependency.name

    def get_preference(
        self,
        resolution,  # type: Optional[Candidate]
        candidates,  # type: Sequence[Candidate]
        information  # type: Sequence[Tuple[Requirement, Candidate]]
    ):
        # type: (...) -> Any
        # Use the "usual" value for now
        return len(candidates)

    def find_matches(self, requirement):
        # type: (Requirement) -> Sequence[Candidate]
        constraint = self._constraints.get(requirement.name, SpecifierSet())
        return requirement.find_matches(constraint)

    def is_satisfied_by(self, requirement, candidate):
        # type: (Requirement, Candidate) -> bool
        return requirement.is_satisfied_by(candidate)

    def get_dependencies(self, candidate):
        # type: (Candidate) -> Sequence[Requirement]
        if self._ignore_dependencies:
            return []
        return candidate.get_dependencies()
