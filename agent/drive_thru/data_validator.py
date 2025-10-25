"""
Data validation and transformation for drive-thru pipeline
"""
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from uuid import UUID, uuid4
import logging
from pydantic import BaseModel, ValidationError, validator
from .order import OrderState, OrderStatus, ConversationMetrics

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error for data pipeline"""
    pass


class DataValidator:
    """Validates and cleans data before database storage"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_conversation_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate conversation data structure and content"""
        try:
            # Required fields
            required_fields = ['session_id', 'conversation_id', 'start_time']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Missing required field: {field}")
            
            # Validate session_id format
            if not self._is_valid_session_id(data['session_id']):
                raise ValidationError("Invalid session_id format")
            
            # Validate conversation_id format
            if not self._is_valid_conversation_id(data['conversation_id']):
                raise ValidationError("Invalid conversation_id format")
            
            # Validate timestamps
            if not isinstance(data['start_time'], datetime):
                try:
                    data['start_time'] = datetime.fromisoformat(data['start_time'])
                except (ValueError, TypeError):
                    raise ValidationError("Invalid start_time format")
            
            if 'end_time' in data and data['end_time']:
                if not isinstance(data['end_time'], datetime):
                    try:
                        data['end_time'] = datetime.fromisoformat(data['end_time'])
                    except (ValueError, TypeError):
                        raise ValidationError("Invalid end_time format")
            
            # Validate numeric fields
            numeric_fields = [
                'total_turns', 'user_turns', 'agent_turns', 'tool_calls_count',
                'successful_tool_calls', 'error_count', 'interruption_count'
            ]
            for field in numeric_fields:
                if field in data:
                    data[field] = self._validate_positive_int(data[field], field)
            
            # Validate boolean fields
            boolean_fields = ['success']
            for field in boolean_fields:
                if field in data:
                    data[field] = bool(data[field])
            
            # Validate float fields
            float_fields = ['duration_seconds', 'sentiment_score']
            for field in float_fields:
                if field in data:
                    data[field] = self._validate_float(data[field], field)
            
            # Validate string fields
            string_fields = ['status', 'location_id']
            for field in string_fields:
                if field in data:
                    data[field] = self._validate_string(data[field], field)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Conversation data validation failed: {e}")
            raise ValidationError(f"Conversation data validation failed: {e}")
    
    def validate_order_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate order data structure and content"""
        try:
            # Required fields
            required_fields = ['order_id', 'conversation_id']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Missing required field: {field}")
            
            # Validate order_id format
            if not self._is_valid_order_id(data['order_id']):
                raise ValidationError("Invalid order_id format")
            
            # Validate status
            if 'status' in data:
                valid_statuses = [status.value for status in OrderStatus]
                if data['status'] not in valid_statuses:
                    raise ValidationError(f"Invalid order status: {data['status']}")
            
            # Validate numeric fields
            numeric_fields = ['total_price', 'item_count']
            for field in numeric_fields:
                if field in data:
                    data[field] = self._validate_positive_float(data[field], field)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Order data validation failed: {e}")
            raise ValidationError(f"Order data validation failed: {e}")
    
    def validate_order_item_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate order item data structure and content"""
        try:
            # Required fields
            required_fields = ['item_id', 'item_type', 'item_name', 'price']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Missing required field: {field}")
            
            # Validate item_type
            valid_item_types = ['regular', 'combo', 'happy_meal', 'drink', 'sauce']
            if data['item_type'] not in valid_item_types:
                raise ValidationError(f"Invalid item_type: {data['item_type']}")
            
            # Validate price
            data['price'] = self._validate_positive_float(data['price'], 'price')
            
            # Validate quantity
            if 'quantity' in data:
                data['quantity'] = self._validate_positive_int(data['quantity'], 'quantity')
            else:
                data['quantity'] = 1
            
            # Validate optional fields
            if 'size' in data and data['size']:
                data['size'] = self._validate_string(data['size'], 'size')
            
            if 'calories' in data and data['calories']:
                data['calories'] = self._validate_positive_int(data['calories'], 'calories')
            
            return data
            
        except Exception as e:
            self.logger.error(f"Order item data validation failed: {e}")
            raise ValidationError(f"Order item data validation failed: {e}")
    
    def validate_metrics_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metrics data structure and content"""
        try:
            # Validate business metrics
            if 'business_metrics' in data:
                business_metrics = data['business_metrics']
                numeric_fields = [
                    'total_orders', 'successful_orders', 'failed_orders', 'cancelled_orders',
                    'total_revenue', 'average_order_value', 'average_conversation_duration',
                    'total_tool_calls', 'successful_tool_calls', 'error_count', 'interruption_count'
                ]
                
                for field in numeric_fields:
                    if field in business_metrics:
                        business_metrics[field] = self._validate_positive_float(
                            business_metrics[field], f"business_metrics.{field}"
                        )
            
            # Validate performance metrics
            if 'performance_metrics' in data:
                performance_metrics = data['performance_metrics']
                float_fields = [
                    'average_response_time', 'tool_call_success_rate',
                    'conversation_success_rate', 'customer_satisfaction_rate'
                ]
                
                for field in float_fields:
                    if field in performance_metrics:
                        performance_metrics[field] = self._validate_float(
                            performance_metrics[field], f"performance_metrics.{field}"
                        )
            
            return data
            
        except Exception as e:
            self.logger.error(f"Metrics data validation failed: {e}")
            raise ValidationError(f"Metrics data validation failed: {e}")
    
    def _is_valid_session_id(self, session_id: str) -> bool:
        """Validate session ID format"""
        if not isinstance(session_id, str):
            return False
        # Session ID should start with 'session_' and contain alphanumeric characters
        pattern = r'^session_\d+_\d+$'
        return bool(re.match(pattern, session_id))
    
    def _is_valid_conversation_id(self, conversation_id: str) -> bool:
        """Validate conversation ID format"""
        if not isinstance(conversation_id, str):
            return False
        # Conversation ID should start with 'C_' and contain alphanumeric characters
        pattern = r'^C_[A-Z0-9]+$'
        return bool(re.match(pattern, conversation_id))
    
    def _is_valid_order_id(self, order_id: str) -> bool:
        """Validate order ID format"""
        if not isinstance(order_id, str):
            return False
        # Order ID should start with 'O_' and contain alphanumeric characters
        pattern = r'^O_[A-Z0-9]+$'
        return bool(re.match(pattern, order_id))
    
    def _validate_positive_int(self, value: Any, field_name: str) -> int:
        """Validate and convert to positive integer"""
        try:
            int_value = int(value)
            if int_value < 0:
                raise ValidationError(f"{field_name} must be non-negative")
            return int_value
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a valid integer")
    
    def _validate_positive_float(self, value: Any, field_name: str) -> float:
        """Validate and convert to positive float"""
        try:
            float_value = float(value)
            if float_value < 0:
                raise ValidationError(f"{field_name} must be non-negative")
            return float_value
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a valid number")
    
    def _validate_float(self, value: Any, field_name: str) -> Optional[float]:
        """Validate and convert to float (allows None)"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a valid number or None")
    
    def _validate_string(self, value: Any, field_name: str) -> Optional[str]:
        """Validate and convert to string (allows None)"""
        if value is None:
            return None
        return str(value).strip()


class DataTransformer:
    """Transforms data between different formats"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def transform_conversation_metrics_to_db(self, metrics: ConversationMetrics, session_id: str) -> Dict[str, Any]:
        """Transform ConversationMetrics to database format"""
        try:
            return {
                'session_id': session_id,
                'conversation_id': metrics.conversation_id,
                'start_time': metrics.start_time,
                'end_time': metrics.end_time,
                'duration_seconds': metrics.duration_seconds,
                'status': 'completed' if metrics.order_success else 'failed',
                'success': metrics.order_success,
                'total_turns': metrics.total_turns,
                'user_turns': metrics.user_turns,
                'agent_turns': metrics.agent_turns,
                'tool_calls_count': metrics.tool_calls_count,
                'successful_tool_calls': metrics.successful_tool_calls,
                'error_count': metrics.error_count,
                'interruption_count': metrics.interruption_count,
                'sentiment_score': metrics.sentiment_score,
                'customer_satisfaction': metrics.customer_satisfaction,
                'feedback': metrics.feedback,
            }
        except Exception as e:
            self.logger.error(f"Failed to transform conversation metrics: {e}")
            raise
    
    def transform_order_state_to_db(self, order_state: OrderState, conversation_id: UUID) -> Dict[str, Any]:
        """Transform OrderState to database format"""
        try:
            return {
                'conversation_id': conversation_id,
                'order_id': order_state.conversation_metrics.conversation_id,
                'status': order_state.status.value,
                'total_price': order_state.total_price,
                'item_count': len(order_state.items),
                'applied_coupons': order_state.applied_coupons,
                'total_discount': order_state.total_discount,
                'final_amount': order_state.final_amount,
            }
        except Exception as e:
            self.logger.error(f"Failed to transform order state: {e}")
            raise
    
    def transform_order_items_to_db(self, order_state: OrderState, order_id: UUID) -> List[Dict[str, Any]]:
        """Transform order items to database format"""
        try:
            items = []
            for item in order_state.items.values():
                item_data = {
                    'order_id': order_id,
                    'item_id': getattr(item, 'meal_id', getattr(item, 'item_id', '')),
                    'item_type': item.type,
                    'item_name': self._get_item_name(item),
                    'size': getattr(item, 'drink_size', getattr(item, 'size', None)),
                    'price': self._calculate_item_price(item),
                    'quantity': 1,
                }
                items.append(item_data)
            return items
        except Exception as e:
            self.logger.error(f"Failed to transform order items: {e}")
            raise
    
    def _get_item_name(self, item) -> str:
        """Extract item name from order item"""
        # McDonald's menu item names
        item_names = {
            'big_mac': 'Big Mac',
            'quarter_pounder': 'Quarter Pounder',
            'mcnuggets_4': 'Chicken McNuggets (4pc)',
            'mcnuggets_6': 'Chicken McNuggets (6pc)',
            'mcnuggets_10': 'Chicken McNuggets (10pc)',
            'mcnuggets_20': 'Chicken McNuggets (20pc)',
            'filet_o_fish': 'Filet-O-Fish',
            'mchicken': 'McChicken',
            'crispy_chicken': 'Crispy Chicken Sandwich',
            'spicy_mchicken': 'Spicy McChicken',
            'hamburger': 'Hamburger',
            'cheeseburger': 'Cheeseburger',
            'fries': 'French Fries',
            'coca_cola': 'Coca-Cola',
            'sprite': 'Sprite',
            'fanta': 'Fanta',
            'coffee': 'Coffee',
            'ice_cream': 'Ice Cream',
            'apple_pie': 'Apple Pie'
        }
        
        try:
            item_id = getattr(item, 'meal_id', getattr(item, 'item_id', ''))
            if item_id in item_names:
                return item_names[item_id]
            else:
                # Fallback to formatted item type
                return item.type.replace('_', ' ').title()
        except Exception:
            return item.type.replace('_', ' ').title()
    
    def _calculate_item_price(self, item) -> float:
        """Calculate item price based on McDonald's menu pricing"""
        # McDonald's menu pricing (approximate US prices)
        pricing = {
            # Combo Meals
            'combo_meal': {
                'big_mac': {'M': 8.99, 'L': 9.99},
                'quarter_pounder': {'M': 8.99, 'L': 9.99},
                'mcnuggets_10': {'M': 8.99, 'L': 9.99},
                'mcnuggets_20': {'M': 8.99, 'L': 9.99},
                'filet_o_fish': {'M': 7.99, 'L': 8.99},
                'mchicken': {'M': 7.99, 'L': 8.99},
                'crispy_chicken': {'M': 7.99, 'L': 8.99},
                'spicy_mchicken': {'M': 7.99, 'L': 8.99},
                'default': {'M': 7.99, 'L': 8.99}
            },
            # Happy Meals
            'happy_meal': {
                'big_mac': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'mcnuggets_4': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'hamburger': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'cheeseburger': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'default': {'S': 4.99, 'M': 5.99, 'L': 6.99}
            },
            # Regular Items
            'regular': {
                'big_mac': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'quarter_pounder': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'mcnuggets_4': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'mcnuggets_6': {'S': 4.99, 'M': 5.99, 'L': 6.99},
                'mcnuggets_10': {'S': 6.99, 'M': 7.99, 'L': 8.99},
                'mcnuggets_20': {'S': 9.99, 'M': 10.99, 'L': 11.99},
                'filet_o_fish': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'mchicken': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'crispy_chicken': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'spicy_mchicken': {'S': 3.99, 'M': 4.99, 'L': 5.99},
                'hamburger': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'cheeseburger': {'S': 2.99, 'M': 3.99, 'L': 4.99},
                'fries': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'coca_cola': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'sprite': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'fanta': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'coffee': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'ice_cream': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'apple_pie': {'S': 1.99, 'M': 2.99, 'L': 3.99},
                'default': {'S': 2.99, 'M': 3.99, 'L': 4.99}
            }
        }
        
        try:
            item_type = item.type
            item_id = getattr(item, 'meal_id', getattr(item, 'item_id', 'default'))
            size = getattr(item, 'drink_size', getattr(item, 'fries_size', getattr(item, 'size', 'M')))
            
            # Get the appropriate size (default to M if not found)
            if size not in ['S', 'M', 'L']:
                size = 'M'
            
            # Get price based on item type and ID
            if item_type in pricing:
                if item_id in pricing[item_type]:
                    return pricing[item_type][item_id].get(size, pricing[item_type]['default'].get(size, 4.99))
                else:
                    return pricing[item_type]['default'].get(size, 4.99)
            else:
                return 4.99  # Default fallback price
                
        except Exception as e:
            self.logger.warning(f"Error calculating price for item {item}: {e}")
            return 4.99  # Safe fallback


# Global instances
data_validator = DataValidator()
data_transformer = DataTransformer()
