"""
Temporary patches for monarchmoney library until PR #175 is merged.
https://github.com/hammem/monarchmoney/pull/175

This module monkey-patches the login methods to:
1. Set trusted_device=True to enable persistent sessions
2. Validate tokenExpiration to ensure we get long-lived tokens
"""

import functools
from typing import Optional
from monarchmoney import MonarchMoney
from monarchmoney.monarchmoney import LoginFailedException


def patch_monarchmoney():
    """Apply patches to monarchmoney library."""
    original_login = MonarchMoney.login

    @functools.wraps(original_login)
    async def patched_login(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        use_saved_session: bool = True,
        save_session: bool = False,
        mfa_secret_key: Optional[str] = None,
    ):
        """Patched login method with trusted_device=True and token validation."""

        # Store original methods to patch specific behaviors
        original_request_async = self.request_async

        async def patched_request_async(api: str, variables: dict):
            """Intercept login requests to modify trusted_device and validate tokens."""

            # Patch loginUser and loginUserWithMfaToken mutations
            if "mutation loginUser" in api or "mutation loginUserWithMfaToken" in api:
                # Set trusted_device to True
                if "trusted_device" in variables:
                    variables["trusted_device"] = True

            # Call original method
            response = await original_request_async(api, variables)

            # Validate token expiration after login mutations
            if ("mutation loginUser" in api or "mutation loginUserWithMfaToken" in api):
                if response and isinstance(response, dict):
                    tokexp = response.get("tokenExpiration")

                    if tokexp not in (None, "null"):
                        raise LoginFailedException(
                            f"Short-lived token returned (tokenExpiration={tokexp}). "
                            "Session will not persist."
                        )

            return response

        # Temporarily replace request_async
        self.request_async = patched_request_async

        try:
            # Call original login
            result = await original_login(
                self,
                email=email,
                password=password,
                use_saved_session=use_saved_session,
                save_session=save_session,
                mfa_secret_key=mfa_secret_key,
            )
            return result
        finally:
            # Restore original method
            self.request_async = original_request_async

    # Apply the patch
    MonarchMoney.login = patched_login


# Automatically apply patches when this module is imported
patch_monarchmoney()
