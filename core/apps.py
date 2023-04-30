from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    # def ready(self):
    #     from core.api.recommand import init_recommand_prompts, check_recommand_prompts_exists
    #     if check_recommand_prompts_exists():
    #         return
    #     from core.api.prompt import Prompt, LANCHED
    #     prompt_list = Prompt.objects.filter(upload_status=LANCHED)
    #     init_recommand_prompts(prompt_list)
