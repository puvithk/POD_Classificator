"""Classification logic for POD documents."""

from typing import Any, Dict, Union
from ..enum.pod_category import PODCategory
from ..schemas.pod_schema import PODExtractionResult


class PODClassification:
    def __init__(self):
        pass

    def classify_pod(self, extracted_info: Union[PODExtractionResult, Dict[str, Any]]) -> Dict[str, Any]:
        """Classify the validity and type of a POD document."""
        if isinstance(extracted_info, PODExtractionResult):
            info_dict = extracted_info.model_dump()
        else:
            info_dict = extracted_info

        default_score = 0.0
        current_info: Dict[str, Any] = {
            "cnNumber": info_dict.get("cn_number", None),
            "hasSignature": info_dict.get("has_signature", False),
            "hasStamp": info_dict.get("has_stamp", False),
            "hasHandwriting": info_dict.get("has_handwriting", False),
            "imageQualityPassed": info_dict.get("image_quality_passed", False),
            "remarksText": info_dict.get("remarks_text", None),
            "deliveryDate": info_dict.get("delivery_date", None),
            "categoryReason": None,
            "categoryScore": default_score,
            "podCategory": "NOT_APPLICABLE",
            "limit_exceed": False,
        }

        # Priority 1: Physical Paper Damage
        if info_dict.get("physical_paper_damage"):
            current_info["podCategory"] = PODCategory.MANUAL_CHECK_REQUIRED.value
            current_info["categoryReason"] = "Physical POD Damage " + (info_dict.get("remarks_text") or "")
            current_info["categoryScore"] += 10
            return current_info

        # Priority 2: Damage and Shortage
        if (
            info_dict.get("business_damage")
            and info_dict.get("business_shortage")
            and info_dict.get("remark") == "DAMAGE_SHORT"
        ):
            current_info["podCategory"] = PODCategory.ISSUE_POD_DAMAGED_AND_SHORT.value
            current_info["categoryReason"] = "POD Damage and Shortage " + (info_dict.get("remarks_text") or "")
            current_info["categoryScore"] += 8
            return current_info

        # Priority 3: Business Damage
        if info_dict.get("business_damage") and info_dict.get("remark") == "DAMAGE":
            current_info["podCategory"] = PODCategory.ISSUE_POD_DAMAGED.value
            current_info["categoryReason"] = "Business POD Damage " + (info_dict.get("remarks_text") or "")
            current_info["categoryScore"] += 5
            return current_info

        # Priority 4: Shortage
        if info_dict.get("business_shortage") and info_dict.get("remark") == "SHORT":
            current_info["podCategory"] = PODCategory.ISSUE_POD_SHORT.value
            current_info["categoryReason"] = "POD Shortage " + (info_dict.get("remarks_text") or "")
            current_info["categoryScore"] += 3
            return current_info

        # Priority 5: Clean POD without any issues with signature and stamp
        if (
            info_dict.get("has_signature")
            and info_dict.get("has_stamp")
            and info_dict.get("has_handwriting")
            and info_dict.get("image_quality_passed")
            and info_dict.get("remark") is None
        ):
            current_info["podCategory"] = PODCategory.CLEAN_POD_SEAL_AND_SIGNATURE.value
            current_info["categoryReason"] = "Clean POD without any issues with signature and stamp"
            current_info["categoryScore"] += 1
            return current_info

        # Priority 6: Clean POD with only Stamp
        if info_dict.get("has_stamp") and info_dict.get("remark") is None and not info_dict.get("has_signature"):
            current_info["podCategory"] = PODCategory.CLEAN_POD_ONLY_SEAL.value
            current_info["categoryReason"] = "Clean POD with stamp only"
            current_info["categoryScore"] += 1
            return current_info

        # Priority 7: Clean POD with only Signature
        if info_dict.get("has_signature") and info_dict.get("remark") is None and not info_dict.get("has_stamp"):
            current_info["podCategory"] = PODCategory.CLEAN_POD_ONLY_SIGNATURE.value
            current_info["categoryReason"] = "Clean POD with signature only"
            current_info["categoryScore"] += 1
            return current_info

        # Priority 8: Clean POD without stamp or signature and no handwritten remarks
        if (
            info_dict.get("remark") is None
            and not info_dict.get("has_stamp")
            and not info_dict.get("has_signature")
            and not info_dict.get("has_handwriting")
        ):
            current_info["podCategory"] = PODCategory.NO_SIGNATURE_NO_STAMP.value
            current_info["categoryReason"] = "POD without stamp or signature"
            current_info["categoryScore"] += 1
            return current_info

        return current_info

