from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class InputRichBlock(TelegramObject):
    """
    This object represents a block in a rich formatted message to be sent. Currently, it can be any of the following types:

     - :class:`litegram.types.input_rich_block_paragraph.InputRichBlockParagraph`
     - :class:`litegram.types.input_rich_block_section_heading.InputRichBlockSectionHeading`
     - :class:`litegram.types.input_rich_block_preformatted.InputRichBlockPreformatted`
     - :class:`litegram.types.input_rich_block_footer.InputRichBlockFooter`
     - :class:`litegram.types.input_rich_block_divider.InputRichBlockDivider`
     - :class:`litegram.types.input_rich_block_mathematical_expression.InputRichBlockMathematicalExpression`
     - :class:`litegram.types.input_rich_block_anchor.InputRichBlockAnchor`
     - :class:`litegram.types.input_rich_block_list.InputRichBlockList`
     - :class:`litegram.types.input_rich_block_block_quotation.InputRichBlockBlockQuotation`
     - :class:`litegram.types.input_rich_block_expandable_block_quotation.InputRichBlockExpandableBlockQuotation`
     - :class:`litegram.types.input_rich_block_pull_quotation.InputRichBlockPullQuotation`
     - :class:`litegram.types.input_rich_block_collage.InputRichBlockCollage`
     - :class:`litegram.types.input_rich_block_slideshow.InputRichBlockSlideshow`
     - :class:`litegram.types.input_rich_block_table.InputRichBlockTable`
     - :class:`litegram.types.input_rich_block_details.InputRichBlockDetails`
     - :class:`litegram.types.input_rich_block_map.InputRichBlockMap`
     - :class:`litegram.types.input_rich_block_buttons.InputRichBlockButtons`
     - :class:`litegram.types.input_rich_block_animation.InputRichBlockAnimation`
     - :class:`litegram.types.input_rich_block_audio.InputRichBlockAudio`
     - :class:`litegram.types.input_rich_block_document.InputRichBlockDocument`
     - :class:`litegram.types.input_rich_block_photo.InputRichBlockPhoto`
     - :class:`litegram.types.input_rich_block_video.InputRichBlockVideo`
     - :class:`litegram.types.input_rich_block_voice_note.InputRichBlockVoiceNote`
     - :class:`litegram.types.input_rich_block_thinking.InputRichBlockThinking`

    Source: https://core.telegram.org/bots/api#inputrichblock
    """
