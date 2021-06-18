from datetime import datetime
from config import db, ma

# Base weapons
class BaseWeapon(db.Model):
    __tablename__ = "base_weapons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    hands = db.Column(db.Integer)
    base_damage_min = db.Column(db.Integer)
    base_damage_max = db.Column(db.Integer)
    damage_type_primary = db.Column(db.String(32))
    damage_type_secondary = db.Column(db.String(32))
    base_weight = db.Column(db.Float)
    base_attacks_per_second = db.Column(db.Float)
    base_hit_chance = db.Column(db.Float)
    description = db.Column(db.String(64))

class view_BaseWeapon(db.Model):
    __tablename__ = "view_base_weapons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    hands = db.Column(db.Integer)
    base_damage_min = db.Column(db.Integer)
    base_damage_max = db.Column(db.Integer)
    damage_type_primary = db.Column(db.String(32))
    damage_type_secondary = db.Column(db.String(32))
    base_weight = db.Column(db.Float)
    base_attacks_per_second = db.Column(db.Float)
    base_hit_chance = db.Column(db.Float)
    description = db.Column(db.String(64))

class BaseWeaponSchema(ma.ModelSchema):
    class Meta:
        model = BaseWeapon
        sqla_session = db.session   

class view_BaseWeaponSchema(ma.ModelSchema):
    class Meta:
        model = view_BaseWeapon
        sqla_session = db.session  

# Base armor
class BaseArmor(db.Model):
    __tablename__ = "base_armors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    base_defense = db.Column(db.Integer)
    description = db.Column(db.String(64))
    base_weight = db.Column(db.Float)
    armor_type = db.Column(db.Integer)
    slot = db.Column(db.Integer)

class BaseArmorSchema(ma.ModelSchema):
    class Meta:
        model = BaseArmor
        sqla_session = db.session   

# Damage Types
class DamageType(db.Model):
    __tablename__ = "damage_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))

class DamageTypeSchema(ma.ModelSchema):
    class Meta:
        model = DamageType
        sqla_session = db.session

# Culture
class Culture(db.Model):
    __tablename__ = "cultures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))

class CultureSchema(ma.ModelSchema):
    class Meta:
        model = Culture
        sqla_session = db.session

# element_types
class ElementType(db.Model):
    __tablename__ = "element_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    status_effect = db.Column(db.Integer)

class view_ElementType(db.Model):
    __tablename__ = "view_element_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    status_effect = db.Column(db.String(64))

class ElementTypeSchema(ma.ModelSchema):
    class Meta:
        model = ElementType
        sqla_session = db.session

class viewElementTypeSchema(ma.ModelSchema):
    class Meta:
        model = view_ElementType
        sqla_session = db.session

# owners
class Owner(db.Model):
    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    culture =db.Column(db.Integer)

class view_Owner(db.Model):
    __tablename__ = "view_owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    culture =db.Column(db.String(64))

class OwnerSchema(ma.ModelSchema):
    class Meta:
        model = Owner
        sqla_session = db.session

class viewOwnerSchema(ma.ModelSchema):
    class Meta:
        model = view_Owner
        sqla_session = db.session

# status_effects
class StatusEffect(db.Model):
    __tablename__ = "status_effects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    base_duration = db.Column(db.Float)
    
class StatusEffectSchema(ma.ModelSchema):
    class Meta:
        model = StatusEffect
        sqla_session = db.session

# ArmorSlot
class ArmorSlot(db.Model):
    __tablename__ = "armor_slots"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

class ArmorSlotSchema(ma.ModelSchema):
    class Meta:
        model = ArmorSlot
        sqla_session = db.session

# ArmorType
class ArmorType(db.Model):
    __tablename__ = "armor_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))

class ArmorTypeSchema(ma.ModelSchema):
    class Meta:
        model = ArmorType
        sqla_session = db.session

# Backpack
class Backpack(db.Model):
    __tablename__ = "backpacks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32))

class BackpackSchema(ma.ModelSchema):
    class Meta:
        model = Backpack
        sqla_session = db.session

# User
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    password_hash = db.Column(db.String(64))
    password_salt = db.Column(db.String(64))
    email = db.Column(db.String(64))

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

# Loadout
class Loadout(db.Model):
    __tablename__ = "loadouts"
    id = db.Column(db.Integer, primary_key=True)
    left_weapon = db.Column(db.Integer)
    right_weapon = db.Column(db.Integer)
    chest_slot = db.Column(db.Integer)
    head_slot = db.Column(db.Integer)
    legs_slot = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class LoadoutSchema(ma.ModelSchema):
    class Meta:
        model = Loadout
        sqla_session = db.session

# UniqueWeapon
class UniqueWeapon(db.Model):
    __tablename__ = "unique_weapons"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), default="")
    description = db.Column(db.String(128))
    level = db.Column(db.Integer)
    added_damage = db.Column(db.Integer)
    base_weapon_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, default=None)
    culture_id = db.Column(db.Integer, default=None)
    element_id = db.Column(db.Integer, default=None)

class UniqueWeaponSchema(ma.ModelSchema):
    class Meta:
        model = UniqueWeapon
        sqla_session = db.session

# UniqueArmor
class UniqueArmor(db.Model):
    __tablename__ = "unique_armor"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), default="")
    description = db.Column(db.String(128))
    level = db.Column(db.Integer)
    added_defense = db.Column(db.Integer)
    base_armor_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, default=None)
    culture_id = db.Column(db.Integer, default=None)

class UniqueArmorSchema(ma.ModelSchema):
    class Meta:
        model = UniqueArmor
        sqla_session = db.session

# Nickname
class Nickname(db.Model):
    __tablename__ = "nicknames"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

class NicknameSchema(ma.ModelSchema):
    class Meta:
        model = Nickname
        sqla_session = db.session