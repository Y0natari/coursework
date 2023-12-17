from filters.admin_filter import IsAdmin
from config.config import Config
from database import db
from utils.api import APIClient
from states.bot_states import Creation

from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.storage import FSMContext
from aiogram import Bot, Dispatcher
from aiogram import types
import aiogram

async def setup_handlers(dp: Dispatcher, bot: Bot):
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        language_code = await db.get_language(message.from_user.id)
        if language_code is None:
            language_code = 'ua'
        config = Config(message.from_user.id, f"languages/{language_code}.ini")
        
        text = await config.get('MAIN_MENU', 'text')
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_med_list'), callback_data='button_med_list'))
        keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_faq'), callback_data='faq'))

        await message.answer(text, reply_markup=keyboard)

    @dp.message_handler(state='*', content_types=types.ContentType.ANY)
    async def procces_message(message: types.Message, state: FSMContext):
        language_code = await db.get_language(message.from_user.id)
        if language_code is None:
            language_code = 'ua'
        config = Config(message.from_user.id, f"languages/{language_code}.ini")
        client = APIClient("http://localhost:8000")
        state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
        current_state = await state.get_state()
        
        if current_state == 'Creation:get_cat_name':
            await client.create_category(message.text)
            async with state.proxy() as deletor:
                msg = deletor['todel']
                cat_id = deletor['cat_id']
            await bot.delete_message(chat_id=message.from_user.id, message_id=msg)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await state.finish()
            
            text_success = await config.get("CREATE_CATEGORIE", "text_success")
            go_to_categorie = await config.get('GO_BACK', 'go_to_categorie')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_to_categorie, callback_data=f'categorie_{cat_id}'))
            
            await bot.send_message(chat_id=message.from_user.id, text=text_success, reply_markup=keyboard)
        
        elif current_state == 'Creation:get_good_name':
            await client.create_category(message.text)
            async with state.proxy() as deletor:
                msg = deletor['todel']
            await bot.delete_message(chat_id=message.from_user.id, message_id=msg)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await state.finish()
            
            text_success = await config.get("CREATE_GOOD", "text_success")
            go_to_categories = await config.get('GO_BACK', 'go_to_categories')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_to_categories, callback_data=f'button_med_list'))
            
            await bot.send_message(chat_id=message.from_user.id, text=text_success, reply_markup=keyboard)

    @dp.callback_query_handler(state='*')
    async def procces_callback(callback: types.CallbackQuery, state: FSMContext):
        language_code = await db.get_language(callback.from_user.id)
        if language_code is None:
            language_code = 'ua'
        config = Config(callback.from_user.id, f"languages/{language_code}.ini")
        
        client = APIClient("http://localhost:8000")
        if callback.data == 'button_med_list':
            categories = await client.get_category_names()
            if len(categories) > 0:
                text_categories = await config.get('MEDICINE', 'text_categories')
                button_create_categorie = await config.get('MEDICINE', 'button_create_categorie')
                go_main_menu = await config.get('GO_BACK', 'go_main_menu')
                
                keyboard = InlineKeyboardMarkup()
                for id, categorie in enumerate(categories, start=1):
                    keyboard.add(InlineKeyboardButton(text=categorie, callback_data=f'categorie_{id}'))
                keyboard.add(InlineKeyboardButton(text=button_create_categorie, callback_data=f'button_create_categorie'))
                keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
                
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text_categories, reply_markup=keyboard)
            else:
                text_categories_empty = await config.get('MEDICINE', 'text_categories_empty')
                button_create_categorie = await config.get('MEDICINE', 'button_create_categorie')
                go_main_menu = await config.get('GO_BACK', 'go_main_menu')
                
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(text=button_create_categorie, callback_data=f'button_create_categorie'))
                keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
                
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text_categories_empty, reply_markup=keyboard)
                
        elif callback.data.startswith('categorie_'):
            cat_id = callback.data.split('_')[1]
            goods = await client.get_drugs_by_category(cat_id)
            if len(goods) > 0:
                text_product = await config.get('MEDICINE', 'text_product')
                button_create_product = await config.get('MEDICINE', 'button_create_product')
                go_to_categories = await config.get('GO_BACK', 'go_to_categories')
                
                keyboard = InlineKeyboardMarkup()
                for good in goods:
                    keyboard.add(InlineKeyboardButton(text=good['name'], callback_data=f'good_{cat_id}_{good["id"]}'))
                keyboard.add(InlineKeyboardButton(text=button_create_product, callback_data=f'buttoncreateproduct_{cat_id}'))
                keyboard.add(InlineKeyboardButton(text=go_to_categories, callback_data=f'button_med_list'))
                
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text_product, reply_markup=keyboard)
            else:
                text_product_empty = await config.get('MEDICINE', 'text_product_empty')
                button_create_product = await config.get('MEDICINE', 'button_create_product')
                go_to_categories = await config.get('GO_BACK', 'go_to_categories')
                
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(text=button_create_product, callback_data=f'buttoncreateproduct_{cat_id}'))
                keyboard.add(InlineKeyboardButton(text=go_to_categories, callback_data=f'button_med_list'))
                
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text_product_empty, reply_markup=keyboard)
        
        elif callback.data.startswith('good_'):
            cat_id = callback.data.split('_')[1]
            prod_id = callback.data.split('_')[2]
            info = await client.get_drug_by_id(prod_id)

            text_id = await config.get("PRODUCT", "text_id") + str(prod_id)
            text_name = await config.get("PRODUCT", "text_name") + str(info[0]['name'])
            text_categorie = await config.get("PRODUCT", "text_categorie") + str(await client.get_category_name_by_id(info[0]['category']))
            text_stock = await config.get("PRODUCT", "text_stock") + str(info[0]['quantity']) + "шт. "
            text_price = await config.get("PRODUCT", "text_price") + str(info[0]['price']) + "$"
            
            result_text = f"{text_id}\n{text_name}\n{text_categorie}\n{text_stock}\n{text_price}"
            
            button_delete_product = await config.get('PRODUCT', 'button_delete_product')
            go_to_categorie = await config.get('GO_BACK', 'go_to_categorie')
                
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=button_delete_product, callback_data=f'button_delete_product_{prod_id}'))
            keyboard.add(InlineKeyboardButton(text=go_to_categorie, callback_data=f'categorie_{cat_id}'))
                
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=result_text, reply_markup=keyboard)
        
        elif callback.data == 'button_create_categorie':
            await Creation.get_cat_name.set()
            text_categorie_name = await config.get('CREATE_CATEGORIE', 'text_categorie_name')
            go_to_categories = await config.get('GO_BACK', 'go_to_categories')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_to_categories, callback_data=f'button_med_list'))
                
            msg = await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text_categorie_name, reply_markup=keyboard)
            async with state.proxy() as deletor:
                deletor['todel'] = msg.message_id
        
        elif callback.data.startswith('buttoncreateproduct_'):
            cat_id = callback.data.split('_')[1]
            await Creation.get_cat_name.set()
            text_good_name = await config.get('CREATE_CATEGORIE', 'text_good_name')
            go_to_categorie = await config.get('GO_BACK', 'go_to_categorie')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_to_categorie, callback_data=f'categorie_{cat_id}'))
                
            msg = await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text_good_name, reply_markup=keyboard)
            async with state.proxy() as deletor:
                deletor['todel'] = msg.message_id
                deletor['cat_id'] = cat_id
        
        elif callback.data == 'faq':
            text = await config.get('FAQ', 'text')
            go_main_menu = await config.get('GO_BACK', 'go_main_menu')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=go_main_menu, callback_data=f'go_main_menu'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text, reply_markup=keyboard)
        
        elif callback.data == 'go_main_menu':
            text = await config.get('MAIN_MENU', 'text')
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_med_list'), callback_data='button_med_list'))
            keyboard.add(InlineKeyboardButton(text=await config.get('MAIN_MENU', 'button_faq'), callback_data='faq'))
            
            await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=text, reply_markup=keyboard)