from frappe.exceptions import ValidationError


class SyncDisabledError(ValidationError):
	pass


class SyncDirectionError(ValidationError):
	pass


class WooCommerceOrderNotFoundError(ValidationError):
	pass
